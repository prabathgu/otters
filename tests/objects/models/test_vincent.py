import pytest
from objects.models.vincent import Vincent
from unittest.mock import Mock, patch
from objects.prompts.tools import ToolsPrompt
import asyncio
from tools.return_type import ToolResult

@pytest.fixture
def vincent():
    # Create a Vincent instance with some mock tools
    mock_tools = [
        {
            'function': {
                'name': 'test-tool',
                'description': 'A test tool'
            }
        }
    ]
    tools_prompt = ToolsPrompt(tools=mock_tools)
    return Vincent(tools_prompt=tools_prompt)

def test_init():
    """Test Vincent initialization"""
    tools = [{'function': {'name': 'test-tool'}}]
    tools_prompt = ToolsPrompt(tools=tools)
    vincent = Vincent(tools_prompt=tools_prompt)
    assert vincent.tools_prompt.tools == tools

def test_process_input_string():
    """Test _process_input with string input"""
    vincent = Vincent()
    step_outputs = {1: "hello", 2: "world"}
    
    # Test basic string replacement
    result = vincent._process_input("Step 1 says {{1}}", step_outputs)
    assert result == "Step 1 says hello"
    
    # Test multiple replacements
    result = vincent._process_input("{{1}} {{2}}", step_outputs)
    assert result == "hello world"
    
    # Test string without replacements
    result = vincent._process_input("No replacements", step_outputs)
    assert result == "No replacements"

def test_process_input_dict():
    """Test _process_input with dictionary input"""
    vincent = Vincent()
    step_outputs = {1: "hello"}
    
    input_dict = {
        "message": "{{1}}",
        "other": "static"
    }
    result = vincent._process_input(input_dict, step_outputs)
    assert result == {
        "message": "hello",
        "other": "static"
    }

def test_process_input_list():
    """Test _process_input with list input"""
    vincent = Vincent()
    step_outputs = {1: "hello"}
    
    input_list = ["{{1}}", "static"]
    result = vincent._process_input(input_list, step_outputs)
    assert result == ["hello", "static"]

@pytest.mark.asyncio
async def test_execute_tool_not_found():
    """Test executing a non-existent tool"""
    vincent = Vincent()
    result: ToolResult = vincent._execute_tool("nonexistent-tool")
    assert not result.success
    assert result.error == "Error: Tool 'nonexistent-tool' not found"

@patch('importlib.import_module')
def test_execute_tool_module_not_found(mock_import):
    """Test executing a tool with missing module"""
    mock_import.side_effect = ImportError()
    vincent = Vincent(tools_prompt=ToolsPrompt([{'function': {'name': 'test-module'}}]))
    
    result: ToolResult = vincent._execute_tool("test-module")
    assert not result.success
    assert result.error == "Error: Module 'tools.test' not found"

@patch('importlib.import_module')
def test_execute_tool_function_not_found(mock_import):
    """Test executing a tool with missing function"""
    mock_module = Mock()
    mock_import.return_value = mock_module
    mock_module.function = Mock(side_effect=AttributeError())
    
    vincent = Vincent(tools_prompt=ToolsPrompt([{'function': {'name': 'test-function'}}]))
    result: ToolResult = vincent._execute_tool("test-function")
    assert not result.success
    assert result.error == "Error: Function 'function' not found in module 'tools.test'"

def test_execute_invalid_plan():
    """Test executing an invalid plan"""
    vincent = Vincent()
    
    # Test with non-dict plan
    with pytest.raises(ValueError):
        vincent.execute("not a dict")
    
    # Test with dict missing steps
    with pytest.raises(ValueError):
        vincent.execute({"not_steps": []})

def test_execute_with_callback():
    """Test execute with callback function"""
    vincent = Vincent(tools_prompt=ToolsPrompt([{'function': {'name': 'test-tool'}}]))
    callback_calls = []
    
    def callback(data):
        callback_calls.append(data)
    
    plan = {
        "steps": [
            {
                "step": 1,
                "tool": "test-tool",
                "required_for_response": True
            }
        ]
    }
    
    # Mock the _execute_tool method
    with patch.object(Vincent, '_execute_tool', return_value=ToolResult.ok("test result")):
        result: Vincent.VincentExecuteResult = vincent.execute(plan, callback=callback)
        print(result)
        # Verify callback was called for step start, complete and final result
        assert len(callback_calls) == 3
        assert callback_calls[0]["type"] == "step_start"
        assert callback_calls[1]["type"] == "step_complete"
        assert callback_calls[2]["type"] == "final_result"
        
        # Verify the result structure
        assert result.completed
        assert len(result.outputs) == 1
        assert result.tools == ["test-tool"]
        assert result.required_outputs == ["Step 1: test result"]

def test_execute_with_error():
    """Test execute when a tool returns an error"""
    vincent = Vincent(tools_prompt=ToolsPrompt([{'function': {'name': 'test-tool'}}]))
    
    plan = {
        "steps": [
            {
                "step": 1,
                "tool": "test-tool"
            }
        ]
    }
    
    # Mock the _execute_tool method to return an error
    with patch.object(Vincent, '_execute_tool', return_value=ToolResult.err("Error: Test error")):
        result: Vincent.VincentExecuteResult = vincent.execute(plan)
        
        # Verify the error handling
        assert not result.completed
        assert len(result.outputs) == 1
        assert result.outputs[0].startswith("Step 1: Error:")

def test_execute_with_image_url():
    """Test execute with image generation result"""
    vincent = Vincent(tools_prompt=ToolsPrompt([{'function': {'name': 'test-tool'}}]))
    
    plan = {
        "steps": [
            {
                "step": 1,
                "tool": "test-tool"
            }
        ]
    }
    
    # Test with image generation tool output
    image_response = {"success": True, "image_url": "test.jpg"}
    with patch.object(Vincent, '_execute_tool', return_value=ToolResult.ok(image_response)):
        result: Vincent.VincentExecuteResult = vincent.execute(plan)
        assert result.outputs[0] == f"Step 1: {image_response}"
    
    # Test with images array output
    images_response = {"images": [{"url": "test2.jpg"}]}
    with patch.object(Vincent, '_execute_tool', return_value=ToolResult.ok(images_response)):
        result: Vincent.VincentExecuteResult = vincent.execute(plan)
        assert result.outputs[0] == f"Step 1: {images_response}"

def test_execute_with_invalid_step():
    """Test execute with an invalid step structure"""
    vincent = Vincent(tools_prompt=ToolsPrompt([{'function': {'name': 'test-tool'}}]))
    
    plan = {
        "steps": [
            "not a dict"  # Invalid step structure
        ]
    }
    
    with pytest.raises(ValueError, match="Expected step to be a dictionary"):
        vincent.execute(plan)

def test_execute_with_original_messages():
    """Test execute with original messages context"""
    vincent = Vincent(tools_prompt=ToolsPrompt([{'function': {'name': 'test-tool'}}]))
    
    plan = {
        "steps": [
            {
                "step": 1,
                "tool": "test-tool"
            }
        ]
    }
    
    original_messages = [
        {"role": "user", "content": "test message"}
    ]
    
    with patch.object(Vincent, '_execute_tool', return_value=ToolResult.ok("test result")):
        result: Vincent.VincentExecuteResult = vincent.execute(plan, original_messages=original_messages)
        assert result.completed
        assert result.outputs == ["Step 1: test result"]

def test_process_input_with_missing_step():
    """Test _process_input with reference to non-existent step"""
    vincent = Vincent()
    step_outputs = {1: "hello"}
    
    # Reference to missing step should leave placeholder unchanged
    result = vincent._process_input("Step {{2}} not found", step_outputs)
    assert result == "Step {{2}} not found"

def test_execute_with_none_input():
    """Test execute_tool with None input"""
    vincent = Vincent(tools_prompt=ToolsPrompt([{'function': {'name': 'test-tool'}}]))
    
    plan = {
        "steps": [
            {
                "step": 1,
                "tool": "test-tool",
                "input": None
            }
        ]
    }
    
    with patch.object(Vincent, '_execute_tool', return_value=ToolResult.ok("test result")) as mock_execute:
        result: Vincent.VincentExecuteResult = vincent.execute(plan)
        mock_execute.assert_called_once_with("test-tool", None, {})
        assert result.completed
        assert result.outputs == ["Step 1: test result"]

def test_execute_with_complex_input():
    """Test execute with complex nested input structure"""
    vincent = Vincent(tools_prompt=ToolsPrompt([{'function': {'name': 'test-tool'}}]))
    
    plan = {
        "steps": [
            {
                "step": 1,
                "tool": "test-tool",
                "input": "first output"
            },
            {
                "step": 2,
                "tool": "test-tool",
                "input": {
                    "message": "Using {{1}}",
                    "data": {
                        "nested": ["{{1}}", "static", {"deep": "{{1}}"}]
                    }
                }
            }
        ]
    }
    
    with patch.object(Vincent, '_execute_tool') as mock_execute:
        mock_execute.side_effect = [ToolResult.ok("first result"), ToolResult.ok("second result")]
        result: Vincent.VincentExecuteResult = vincent.execute(plan)
        
        # Verify the second call had properly processed input
        expected_processed_input = {
            "message": "Using first result",
            "data": {
                "nested": ["first result", "static", {"deep": "first result"}]
            }
        }
        mock_execute.assert_called_with("test-tool", expected_processed_input, {1: "first result"})

@pytest.mark.asyncio
async def test_execute_tool_async():
    """Test executing an async tool function"""
    vincent = Vincent(tools_prompt=ToolsPrompt([{'function': {'name': 'test-async'}}]))

    async def async_tool():
        return "async result"

    with patch('importlib.import_module') as mock_import:
        mock_module = Mock()
        mock_import.return_value = mock_module
        mock_module.async_fn = async_tool

        result = vincent._execute_tool("test-async")
        if asyncio.iscoroutine(result):
            result = await result
        assert result == "async result"

@pytest.mark.asyncio
async def test_execute_tool_async_with_input():
    """Test executing an async tool function with input"""
    vincent = Vincent(tools_prompt=ToolsPrompt([{'function': {'name': 'test-async'}}]))

    async def async_tool(input_data):
        return f"async result with {input_data}"

    with patch('importlib.import_module') as mock_import:
        mock_module = Mock()
        mock_import.return_value = mock_module
        mock_module.async_fn = async_tool

        result = vincent._execute_tool("test-async", "test input")
        if asyncio.iscoroutine(result):
            result = await result
        assert result == "async result with test input"

@pytest.mark.asyncio
async def test_execute_tool_async_with_dict_input():
    """Test executing an async tool function with dictionary input"""
    vincent = Vincent(tools_prompt=ToolsPrompt([{'function': {'name': 'test-async'}}]))

    async def async_tool(**kwargs):
        return f"async result with {kwargs['data']}"

    with patch('importlib.import_module') as mock_import:
        mock_module = Mock()
        mock_import.return_value = mock_module
        mock_module.async_fn = async_tool

        result = vincent._execute_tool("test-async", {"data": "test"})
        if asyncio.iscoroutine(result):
            result = await result
        assert result == "async result with test"

def test_execute_tool_general_exception():
    """Test executing a tool that raises a general exception"""
    vincent = Vincent(tools_prompt=ToolsPrompt([{'function': {'name': 'test-error'}}]))
    
    def error_tool():
        raise Exception("Unexpected error")
    
    with patch('importlib.import_module') as mock_import:
        mock_module = Mock()
        mock_import.return_value = mock_module
        mock_module.error = error_tool
        
        result: ToolResult = vincent._execute_tool("test-error")
        assert not result.success
        assert result.error == "Error: Executing 'test-error' failed with: Unexpected error"

def test_execute_with_invalid_message_content():
    """Test execute with invalid message content"""
    vincent = Vincent(tools_prompt=ToolsPrompt([{'function': {'name': 'test-tool'}}]))
    
    plan = {
        "steps": [
            {
                "step": 1,
                "tool": "test-tool"
            }
        ]
    }
    
    # Test with invalid message content (neither dict nor str)
    original_messages = [{"content": 123}]  # Invalid content type
    
    with patch.object(Vincent, '_execute_tool', return_value=ToolResult.ok("test result")):
        result: Vincent.VincentExecuteResult = vincent.execute(plan, original_messages=original_messages)
        assert result.completed
        assert result.outputs == ["Step 1: test result"]

def test_process_input_invalid_type():
    """Test _process_input with an invalid input type"""
    vincent = Vincent()
    step_outputs = {1: "hello"}
    
    # Test with an invalid input type (e.g., an integer)
    result = vincent._process_input(42, step_outputs)
    assert result == 42  # Should return the input unchanged

def test_execute_tool_sync_with_dict_input():
    """Test executing a synchronous tool function with dictionary input"""
    vincent = Vincent(tools_prompt=ToolsPrompt([{'function': {'name': 'test-sync'}}]))
    
    def sync_tool(**kwargs):
        return f"sync result with {kwargs['data']}"
    
    with patch('importlib.import_module') as mock_import:
        mock_module = Mock()
        mock_import.return_value = mock_module
        mock_module.sync = sync_tool
        
        result = vincent._execute_tool("test-sync", {"data": "test"})
        assert result == "sync result with test"