import json
from typing import List, Dict, Any, Callable, Optional
import weave
from weave import Model
from weave.integrations.bedrock.bedrock_sdk import patch_client
import boto3
import os

from objects.prompts.winston import WinstonPlanAnswerPrompt, WinstonAnswerWithResultsPrompt
from objects.models.vincent import Vincent
from utils.helpers import clean_claude_json
from objects.models.finetuned import FinetunedModel
from tools.vector_search import initialize_or_load_vector_db
class Winston(Model):
    prompt_plan_answer: WinstonPlanAnswerPrompt = WinstonPlanAnswerPrompt()
    prompt_answer_with_results: WinstonAnswerWithResultsPrompt = WinstonAnswerWithResultsPrompt()
    vincent: Vincent = Vincent()
    bedrock_client: Optional[boto3.client] = None
    finetuned_model: Optional[FinetunedModel] = None
    use_finetuned: bool = False
    model_id: str = "gpt-4o"
    
    def __init__(
        self, 
        model_id: str = "gpt-4o",
        auto_execute: bool = True,
        vincent: Vincent = None,
        region_name: str = os.getenv("AWS_DEFAULT_REGION"),
        use_finetuned: bool = False,
    ):
        super().__init__()
        self.vincent = vincent if vincent is not None else Vincent()
        self.model_id = model_id
        self._auto_execute = auto_execute
        self.bedrock_client = boto3.client('bedrock-runtime', region_name=region_name)
        
        patch_client(self.bedrock_client)
        
        initialize_or_load_vector_db('/Users/wylerzahm/Desktop/projects/fc2025-space-agent/objects/datasets/knowledge_base.md')
        
        if use_finetuned:
            self.finetuned_model = FinetunedModel()




    ##### 1. NEW QUERY ENTRY POINT #####
    @weave.op(name="winston-predict")
    def predict(self, messages: List[Dict[str, str]], callback: Optional[Callable] = None) -> Dict[str, Any]:
        """Alias for process method"""
        return self.process(messages[0]['content'], callback)

    ##### 2. QUERY PROCESSING ENTRY POINT #####
    @weave.op(name="winston-process")
    def process(
        self, 
        query: str, 
        callback: Callable[[Dict[str, Any]], None] = None
    ) -> Dict[str, Any]:
        """
        Main entry point for processing messages. Handles the high-level flow of:
        1. Getting initial response
        2. Executing plans if needed
        3. Getting final answer
        """
        # Get initial response
        response = self._plan_or_answer(query)
        #print("***** Initial response:", response)
        
        # If we got a plan and should execute it
        if response.get('type') == 'plan':
            # Execute the plan and get the updated response with process info
            executed_plan_response = self._execute_plan(response)
            #print("***** Executed plan response:", executed_plan_response)

            # If execution occurred (indicated by presence of process key from _execute_plan)
            if executed_plan_response and 'process' in executed_plan_response:
                # Get the final answer from the LLM using the updated messages
                if self.finetuned_model:
                    final_response = self._solve_with_results_finetuned(query, executed_plan_response['process']['execution_summary'])
                else:
                    final_response = self._solve_with_results(query, executed_plan_response['process']['execution_summary'])
                #print("***** Final response after execution:", final_response)
                
                # Carry over the detailed process information from the execution
                final_response['process'] = executed_plan_response['process']
                
                return final_response
            else:
                 # If execution failed very early, return the initial response which might have some error info
                 return executed_plan_response or response
        
        else:
            # If it wasn't a plan or auto_execute is off, return the initial response
            return response

    ##### 3. PLAN OR ANSWER #####
    @weave.op(name="winston-solve")
    def _plan_or_answer(
        self, 
        query: str, 
        execution_results: Vincent.VincentExecuteResult = None
    ) -> Dict[str, Any]:

        # Generate tool descriptions
        tool_descriptions = self.vincent.tools_prompt.get_tools_descriptions()

        # Generate the dynamic system message, ensure system message is always first
        system_message = self.prompt_plan_answer.system_prompt(tool_descriptions)   
        messages_for_run = [
            {"role": "system", "content": system_message}, 
            {"role": "user", "content": query}
        ]

        # Generate response
        response = self._generate_response(messages_for_run)
        return response

    ##### 4. EXECUTE PLAN #####
    @weave.op(name="winston-execute")
    def _execute_plan(
        self,
        plan_response: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Execute a plan, update its process key, and return it."""
        # Get the original plan steps
        original_steps = plan_response.get('content', {}).get('steps', [])
        
        # Execute the plan using Vincent
        execution_result: Vincent.VincentExecuteResult = self.vincent.execute(plan_response['content'])
        
        # Prepare detailed process information
        tools_used = []
        steps_taken = []
        execution_summary = []

        if execution_result:
            if execution_result.completed:
                summary_status = "Plan execution completed successfully."
            else:
                summary_status = f"Plan execution failed at step {execution_result.failure_step}."
            execution_summary.append(summary_status)

            # Process executed steps
            for i, output in enumerate(execution_result.outputs):
                step_def = original_steps[i]
                tool_name = step_def.get('tool')
                status = 'completed' if execution_result.completed else ('failed' if i + 1 == execution_result.failure_step else 'completed')
                step_summary = f"Step {i + 1} ({tool_name}): {output}" 
                if status == 'failed':
                    step_summary += " (Failed)"
                execution_summary.append(step_summary)
                
                if tool_name:
                    tools_used.append(tool_name)
                    steps_taken.append({
                        'step': i + 1,
                        'tool': tool_name,
                        'input': step_def.get('input', {}),
                        'output': output,
                        'status': status,
                        'reason': step_def.get('reason', '')
                    })

            # Add unexecuted steps
            if not execution_result.completed:
                for i in range(len(execution_result.outputs), len(original_steps)):
                    step_def = original_steps[i]
                    tool_name = step_def.get('tool')
                    step_summary = f"Step {i + 1} ({tool_name}): Not executed"
                    execution_summary.append(step_summary)
                    if tool_name:
                        # We might still want to list the tool even if not used
                        # tools_used.append(tool_name) 
                        steps_taken.append({
                            'step': i + 1,
                            'tool': tool_name,
                            'input': step_def.get('input', {}),
                            'output': None,
                            'status': 'not_executed',
                            'reason': step_def.get('reason', '')
                        })
            
            # Update the process key in the original plan_response
            plan_response['process'] = {
                'tools_used': list(set(tools_used)), # Unique tools used
                'reasoning': 'Plan executed with results',
                'steps_taken': steps_taken,
                'execution_summary': execution_summary
            }

        else: # Handle case where execution didn't even start or returned None
            plan_response['process'] = {
                'tools_used': [],
                'reasoning': 'Plan execution failed or did not occur',
                'steps_taken': [],
                'execution_summary': ["Plan execution failed or did not occur."]
            }
            
        return plan_response # Return the plan_response with populated process info

    ##### 5. SOLVE WITH RESULTS #####
    @weave.op(name="winston-solve-with-results")
    def _solve_with_results(
        self, 
        query: str,
        execution_results: List[str],
    ) -> Dict[str, Any]:

        # Generate the dynamic system message, ensure system message is always first
        system_message = self.prompt_answer_with_results.system_prompt(str(execution_results))
        # Generate the messages for the LLM run
        messages_for_run = [
            {"role": "system", "content": system_message}, 
            {"role": "user", "content": query}
        ]

        # Generate response
        response = self._generate_response(messages_for_run)
        return response
    





    ############ DO NOT MODIFY BELOW THIS LINE ############
    # Evaluation results not guaranteed if this is modified.
    @weave.op(name="winston-solve-finetuned")
    def _solve_with_results_finetuned(
        self, 
        query: str,
        execution_results: List[str],
    ) -> Dict[str, Any]:

        # Generate the dynamic system message, ensure system message is always first
        response = self.finetuned_model.predict(query, str(execution_results))

        final_response = {
            'type': 'answer',
            'content': {
                'message': response,
                'reason': 'Finetuned model response'
            },
        }
        return final_response

    @weave.op(name="winston-generate_response")
    def _generate_response(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        try:
            body_unparsed = None
            processed_messages = []
            for msg in messages:
                content = msg['content']
                if isinstance(content, dict):
                    content = str(content)
                processed_messages.append({
                    "role": msg['role'],
                    "content": content
                })

            # Convert messages to Claude format
            claude_messages = []
            system_message = None
            
            for msg in processed_messages:
                if msg['role'] == 'system':
                    system_message = msg['content']
                else:
                    claude_messages.append({
                        "role": msg['role'],
                        "content": msg['content']
                    })

            # Prepare the request body for Bedrock
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4000,
                "temperature": 0.7,
                "messages": claude_messages
            }
            
            if system_message:
                request_body["system"] = system_message

            # Make the Bedrock API call
            try:
                response = self.bedrock_client.invoke_model(
                    modelId=self.model_id,
                    body=json.dumps(request_body)
                )
            except Exception as e:
                print(f"Error invoking model: {e}")
                raise e

            # Parse the response
            body_unparsed = response['body'].read()
            response_body = json.loads(body_unparsed)
            content = response_body['content'][0]['text']
            
            # Clean the content by removing markdown code block markers and extracting JSON
            cleaned_content = clean_claude_json(content)
            
            # Parse the JSON response from the model
            result = json.loads(cleaned_content)['result']

            # If it's a plan from the LLM, potentially update the process info based on steps
            if result.get('type') == 'plan' and 'steps' in result.get('content', {}):
                 steps = result['content']['steps']
                 tools_used = [step.get('tool') for step in steps if step.get('tool')]
                 # Update process info for the plan
                 result['process'] = {
                     'tools_used': list(set(tools_used)),
                     'reasoning': 'Plan created by LLM to answer query',
                     'steps_taken': steps, # Initially, steps_taken are just the planned steps
                     'execution_summary': [] # No execution summary yet
                 }
            else:
                result['process'] = {
                    'tools_used': [],
                    'reasoning': '',
                    'steps_taken': [],
                    'execution_summary': []
                }
            
            return result
                
        except Exception as e:
            # Return a properly structured error response, including a process key
            return {
                'type': 'answer',
                'content': {
                    'message': f'Error generating response: {str(e)}, {body_unparsed}',
                    'reason': 'Error during response generation'
                },
                'process': {
                    'tools_used': [],
                    'reasoning': f'Error during response generation: {str(e)}',
                    'steps_taken': [],
                    'execution_summary': [f'Error during response generation: {str(e)}']
                }
            }
    #######################################################