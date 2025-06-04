import weave
from weave import Model
import importlib
import asyncio
import json
from typing import List, Dict, Any, Union, Callable, Optional
from objects.prompts.tools import ToolsPrompt
from tools.return_type import ToolResult

class Vincent(Model):
    tools_prompt: ToolsPrompt = ToolsPrompt()

    def __init__(self, tools_prompt: ToolsPrompt = None):
        super().__init__()
        self.tools_prompt = tools_prompt if tools_prompt is not None else ToolsPrompt()
    
    class VincentExecuteResult:
        def __init__(
            self,
            outputs: List[str],
            required_outputs: Optional[List[str]],
            tools: List[str],
            completed: bool,
            failure_step: Optional[int]
        ):
            self.outputs = outputs
            self.required_outputs = required_outputs
            self.tools = tools
            self.completed = completed
            self.failure_step = failure_step

        def __str__(self) -> str:
            """String representation for print() and str()"""
            if self.completed:
                return json.dumps({
                    "completed": self.completed,
                    "outputs": self.outputs,
                    "required_outputs": self.required_outputs,
                    "tools": self.tools,
                })
            else:
                return json.dumps({
                    "completed": self.completed,
                    "outputs": self.outputs,
                    "required_outputs": self.required_outputs,
                    "tools": self.tools,
                    "failure_step": self.failure_step
                })
            
        def __repr__(self) -> str:
            """String representation for direct access"""
            return self.__str__()

    @weave.op(name="vincent-execute")
    def execute(self, plan: Dict[str, Any]) -> VincentExecuteResult:
        if not isinstance(plan, dict) or 'steps' not in plan:
            raise ValueError(f"Expected plan to be a dictionary with a 'steps' key, but got {type(plan)}")
        
        steps = plan['steps']
        last_message_content = ""
        context = str(last_message_content) if isinstance(last_message_content, (dict, str)) else ""
        outputs = []
        tools_used = []
        step_outputs = {}
        required_outputs = []
        execution_failed = False
        failure_step = None

        # Create event loop for async execution if needed
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        for step in steps:
            if not isinstance(step, dict):
                raise ValueError(f"Expected step to be a dictionary, but got {type(step)}")
            
            step_number = step['step']
            required = step.get('required_for_response', False)
            
            # If execution has already failed, mark remaining steps as not executed
            if execution_failed:
                step_output = f"Step {step_number}: Not executed due to previous failure at step {failure_step}"
                outputs.append(step_output)
                if required:
                    required_outputs.append(step_output)
                continue
            
            # Process the input only if it exists in the step
            input_data = step.get('input')
            processed_input = self._process_input(input_data, step_outputs) if input_data is not None else None
            
            # Create a copy of step_outputs for this tool execution, excluding the current step
            current_step_outputs = {k: v for k, v in step_outputs.items() if k < step_number}
            
            tool_result = self._execute_tool(step['tool'], processed_input, current_step_outputs)
            
            # If tool_result is a coroutine, await it
            if asyncio.iscoroutine(tool_result):
                try:
                    tool_result = loop.run_until_complete(tool_result)
                except Exception as e:
                    tool_result = ToolResult.err(f"Error executing async tool: {str(e)}")
            
            # Handle the ToolResult
            if not tool_result.success:
                execution_failed = True
                failure_step = step_number
                error_message = f"Step {step_number}: {tool_result.error}"
                outputs.append(error_message)
                
                context += f"\nExecution failed: {error_message}"
                if required:
                    required_outputs.append(error_message)
                continue
            
            # Handle successful execution
            step_output = f"Step {step_number}: {tool_result.data}"
            outputs.append(step_output)
            
            # If step is required, add to required_outputs
            if required:
                required_outputs.append(step_output)
            
            context += f"\nStep {step_number} output: {tool_result.data}"
            tools_used.append(step['tool'])
            step_outputs[step_number] = tool_result.data

        final_result = Vincent.VincentExecuteResult(
            outputs= outputs,
            required_outputs= required_outputs if required_outputs else None,
            tools= tools_used,
            completed= not execution_failed,
            failure_step= failure_step if execution_failed else None,
        )

        return final_result

    @weave.op(name="vincent-process_input")
    def _process_input(self, input_data: Any, step_outputs: Dict[int, Any]) -> Any:
        if isinstance(input_data, str):
            # Replace all occurrences of {{step_number}} in the string
            for step_number, output in step_outputs.items():
                placeholder = f"{{{{{step_number}}}}}"
                if placeholder in input_data:
                    input_data = input_data.replace(placeholder, str(output))
            return input_data
        elif isinstance(input_data, dict):
            return {k: self._process_input(v, step_outputs) for k, v in input_data.items()}
        elif isinstance(input_data, list):
            return [self._process_input(item, step_outputs) for item in input_data]
        else:
            return input_data
    
    @weave.op(name="vincent-execute_tool")
    def _execute_tool(self, tool_name: str, processed_input: Union[str, Dict[str, Any], None] = None, step_outputs: Dict[int, Any] = {}) -> ToolResult:
        tool = next((t for t in self.tools_prompt.tools if t['function']['name'] == tool_name), None)
        if not tool:
            return ToolResult.err(f"Tool '{tool_name}' not found")

        # Parse the tool name to get the module and function
        module_name, function_name = tool_name.split('-')
        
        try:
            # Dynamically import the module
            module = importlib.import_module(f"tools.{module_name}")
            
            # Get the function from the module
            # Add '_fn' suffix if the function name is a Python keyword
            if function_name == 'async':
                function_name = 'async_fn'
            tool_function = getattr(module, function_name)
            
            # Execute the function with or without input
            if asyncio.iscoroutinefunction(tool_function):
                # Create coroutine based on input type
                if processed_input is None:
                    coro = tool_function()
                elif isinstance(processed_input, dict):
                    coro = tool_function(**processed_input)
                else:
                    coro = tool_function(processed_input)
                
                try:
                    # Try to get the current event loop
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        # If we're in an async context, just return the coroutine
                        # It will be awaited by the caller
                        return coro
                    else:
                        # If we're not in an async context, run the coroutine
                        return loop.run_until_complete(coro)
                except RuntimeError:
                    # If no event loop exists, create one
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        return loop.run_until_complete(coro)
                    finally:
                        loop.close()
            else:
                # For sync functions, execute normally
                if processed_input is None:
                    return tool_function()
                elif isinstance(processed_input, dict):
                    return tool_function(**processed_input)
                else:
                    return tool_function(processed_input)
            
        except ImportError:
            return ToolResult.err(f"Module 'tools.{module_name}' not found")
        except AttributeError:
            return ToolResult.err(f"Function '{function_name}' not found in module 'tools.{module_name}'")
        except Exception as e:
            return ToolResult.err(f"Executing '{tool_name}' failed with: {str(e)}")
