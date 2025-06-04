import pytest
from objects.models.winston import Winston
from objects.models.vincent import Vincent
from objects.prompts.tools import ToolsPrompt
from unittest.mock import Mock, patch, MagicMock
import json
from typing import List, Dict, Any

@pytest.fixture
def mock_tools():
    return [{
        'function': {
            'name': 'test_tool',
            'description': 'A test tool',
            'parameters': {
                'properties': {
                    'param1': {
                        'type': 'string',
                        'description': 'Test parameter',
                        'enum': ['option1', 'option2']
                    }
                }
            }
        }
    }]

@pytest.fixture
def winston(mock_tools: List[Dict[str, Any]]):
    vincent_instance = Vincent(tools_prompt=ToolsPrompt(tools=mock_tools))
    winston_instance = Winston(vincent=vincent_instance)
    return winston_instance

@pytest.fixture
def sample_messages():
    return [
        {"role": "user", "content": "Hello, how are you?"}
    ]

def test_winston_initialization(mock_tools):
    vincent_instance = Vincent(tools_prompt=ToolsPrompt(tools=mock_tools))
    winston = Winston(model_id="test-model", vincent=vincent_instance, auto_execute=False)
    assert winston.vincent.tools_prompt.tools == mock_tools
    assert winston.model_id == "test-model"
    assert winston.auto_execute == False
    assert winston.vincent is not None
    assert winston.jimmie is not None


def test_generate_tool_descriptions(winston: Winston):
    descriptions = winston.vincent.tools_prompt.get_tools_descriptions()
    assert "test_tool" in descriptions
    assert "Test parameter" in descriptions
    assert "Options: ['option1', 'option2']" in descriptions

@patch('litellm.completion')
def test_generate_response_success(mock_completion, winston):
    mock_response = MagicMock()
    mock_response.choices[0].message.content = json.dumps({
        "type": "answer",
        "content": {
            "message": "Test message",
            "reason": "Test reason"
        }
    })
    mock_completion.return_value = mock_response

    messages = [{"role": "user", "content": "test"}]
    response = winston._generate_response(messages)

    assert response["type"] == "answer"
    assert response["content"]["message"] == "Test message"
    assert response["content"]["reason"] == "Test reason"

@patch('litellm.completion')
def test_generate_response_plan(mock_completion, winston):
    mock_response = MagicMock()
    mock_response.choices[0].message.content = json.dumps({
        "type": "plan",
        "content": {
            "steps": [
                {
                    "step": 1,
                    "tool": "test_tool",
                    "input": "test input",
                    "reason": "test reason",
                    "required_for_response": True
                }
            ]
        }
    })
    mock_completion.return_value = mock_response

    messages = [{"role": "user", "content": "test"}]
    response = winston._generate_response(messages)

    assert response["type"] == "plan"
    assert "steps" in response["content"]

@patch('utils.memory.retrieve_memories')
def test_get_relevant_memories(mock_retrieve_memories, winston):
    with patch('objects.models.winston.retrieve_memories') as mock_retrieve:
        mock_retrieve.return_value = ["Memory 1", "Memory 2"]
        messages = [{"role": "user", "content": "test query"}]
        
        memories = winston._get_relevant_memories(messages)
        
        assert len(memories) == 2
        assert "Memory 1" in memories
        mock_retrieve.assert_called_once_with(query="test query", k=3)

@patch('objects.models.winston.Winston._generate_response')
@patch('objects.models.winston.Winston._execute_plan')
def test_process_with_plan_execution(mock_execute_plan, mock_generate_response, winston):
    # Mock the initial response as a plan
    mock_generate_response.side_effect = [
        # First response - the plan
        {
            "type": "plan",
            "content": {
                "steps": [{"step": 1, "tool": "test_tool"}]
            }
        },
        # Second response - after execution
        {
            "type": "answer",
            "content": {
                "message": "Final response",
                "reason": "Test reason"
            }
        }
    ]
    
    # Mock the execution result
    mock_execute_plan.return_value = Vincent.VincentExecuteResult(
        completed=True,
        required_outputs=["Execution result"],
        outputs=["Step 1: Execution result"],
        tools=["test_tool"],
        failure_step=None
    )
    
    messages = [{"role": "user", "content": "test command"}]
    callback = Mock()
    
    result = winston.process(messages, callback)
    
    # Verify the plan was executed
    mock_execute_plan.assert_called_once()
    
    # Verify _generate_response was called twice
    assert mock_generate_response.call_count == 2
    
    # Verify the final result
    assert result["type"] == "answer"
    assert result["content"]["message"] == "Final response"

@patch('objects.models.jimmie.Jimmie.check_and_save_interesting_info')
def test_process_with_memory(mock_check_save, winston):
    mock_check_save.return_value = ["New memory"]
    messages = [{"role": "user", "content": "test"}]
    callback = Mock()
    
    with patch.object(winston, '_generate_response') as mock_generate:
        mock_generate.return_value = {
            "type": "answer",
            "content": {
                "message": "Test response",
                "reason": "Test reason"
            }
        }
        
        winston.process(messages, callback)
        
        # Verify memory functions were called
        mock_check_save.assert_called_once_with("test")
        callback.assert_called_with({
            'type': 'memory_update',
            'content': ['New memory']
        })

@patch('objects.models.winston.Winston.process')
def test_predict_alias(mock_process, winston):
    messages = [{"role": "user", "content": "test"}]
    callback = Mock()
    
    expected_response = {
        "type": "answer",
        "content": {
            "message": "Test response",
            "reason": "Test reason"
        }
    }
    
    mock_process.return_value = expected_response
    
    result = winston.predict(messages, callback)
    
    mock_process.assert_called_once_with(messages, callback)
    assert result == expected_response

def test_solve_with_execution_results(winston):
    messages = [{"role": "user", "content": "test"}]
    execution_results = Vincent.VincentExecuteResult(
        required_outputs=["Result 1", "Result 2"],
        outputs=["Result 1", "Result 2"],
        tools=["test_tool"],
        completed=True,
        failure_step=None
    )
    
    with patch.object(winston, '_generate_response') as mock_generate:
        mock_generate.return_value = {
            "type": "answer",
            "content": {
                "message": "Test response",
                "reason": "Test reason"
            }
        }
        
        result = winston._solve(messages, execution_results=execution_results)
        
        # Verify execution results were included in messages
        mock_generate.assert_called_once()
        call_args = mock_generate.call_args[0][0]
        assert any("Result 1" in msg['content'] for msg in call_args)
        assert any("Result 2" in msg['content'] for msg in call_args)
        
        # Verify response was properly formatted
        assert result["type"] == "answer"
        assert result["content"]["message"] == "Test response"

def test_solve_with_dict_response_content(winston):
    messages = [{"role": "user", "content": "test"}]
    
    with patch.object(winston, '_generate_response') as mock_generate:
        # Test nested content structure
        mock_generate.return_value = {
            "type": "answer",
            "content": {
                "content": {
                    "message": "Nested message",
                    "reason": "Nested reason"
                }
            }
        }
        
        result = winston._solve(messages)
        
        assert result["type"] == "answer"
        assert result["content"]["message"] == "Nested message"
        assert result["content"]["reason"] == "Nested reason"

@patch('litellm.completion')
def test_generate_response_invalid_json(mock_completion, winston):
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Invalid JSON"
    mock_completion.return_value = mock_response

    messages = [{"role": "user", "content": "test"}]
    response = winston._generate_response(messages)

    assert response["type"] == "error"
    assert "Failed to parse JSON response" in response["content"]["message"]

@patch('litellm.completion')
def test_generate_response_invalid_structure(mock_completion, winston):
    mock_response = MagicMock()
    mock_response.choices[0].message.content = json.dumps({
        "invalid": "structure"
    })
    mock_completion.return_value = mock_response

    messages = [{"role": "user", "content": "test"}]
    response = winston._generate_response(messages)

    assert response["type"] == "error"
    assert "Invalid response structure" in response["content"]["message"]

@patch('litellm.completion')
def test_generate_response_exception(mock_completion, winston):
    mock_completion.side_effect = Exception("Test error")

    messages = [{"role": "user", "content": "test"}]
    response = winston._generate_response(messages)

    assert response["type"] == "error"
    assert "Test error" in response["content"]["message"]

def test_execute_plan(winston, mock_vincent_execute_result):
    plan_response = {
        "type": "plan",
        "content": {
            "steps": [{"step": 1, "tool": "test_tool"}]
        }
    }
    messages = [{"role": "user", "content": "test"}]
    callback = Mock()
    
    with patch('objects.models.vincent.Vincent.execute') as mock_execute:
        mock_execute.return_value = mock_vincent_execute_result(
            completed=True,
            required_outputs=["Result"],
            outputs=["Step 1: Result"],
            tools=["test_tool"],
            failure_step=None
        )
        
        result = winston._execute_plan(plan_response, messages, callback)
        
        mock_execute.assert_called_once()
        assert result.completed == True
        assert "Result" in result.required_outputs
        assert len(messages) == 2  # Original message + execution results
