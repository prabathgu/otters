import os
import sys
import pytest
from unittest.mock import patch, Mock

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the project root to the Python path
sys.path.insert(0, project_root)

@pytest.fixture(autouse=True)
def mock_litellm():
    """Mock litellm calls for all tests"""
    with patch('litellm.completion') as mock_completion, \
         patch('litellm.embedding') as mock_embedding:
        
        # Mock completion response
        mock_completion_response = Mock()
        mock_completion_response.choices = [
            Mock(message=Mock(content="Test response"))
        ]
        mock_completion.return_value = mock_completion_response
        
        # Mock embedding response
        mock_embedding.return_value = {
            'data': [{
                'embedding': [0.1] * 1536  # Standard OpenAI embedding size
            }]
        }
        
        yield

@pytest.fixture(autouse=True)
def mock_openai():
    """Mock OpenAI client for all tests"""
    with patch('openai.OpenAI') as mock_client:
        # Configure the mock client
        mock_instance = Mock()
        mock_client.return_value = mock_instance
        
        # Mock chat completion
        mock_chat_response = Mock()
        mock_chat_response.choices = [
            Mock(message=Mock(content="Test response"))
        ]
        mock_instance.chat.completions.create.return_value = mock_chat_response
        
        yield mock_client

@pytest.fixture(autouse=True)
def setup_test_env():
    """Setup test environment variables"""
    # Set dummy environment variables that won't be used due to mocking
    os.environ['OPENAI_API_KEY'] = 'dummy_key'
    os.environ['WEAVE_API_KEY'] = 'dummy_key'
    os.environ['X_API_KEY'] = 'dummy_key'
    os.environ['X_API_SECRET'] = 'dummy_key'
    os.environ['X_ACCESS_TOKEN'] = 'dummy_key'
    os.environ['X_ACCESS_TOKEN_SECRET'] = 'dummy_key'
    os.environ['SLACK_BOT_TOKEN'] = 'dummy_key'
    os.environ['GOOGLE_CLIENT_ID'] = 'dummy_key'
    os.environ['GOOGLE_CLIENT_SECRET'] = 'dummy_key'
    os.environ['SERPAPI_API_KEY'] = 'dummy_key'

@pytest.fixture
def mock_vincent_execute_result():
    """Mock Vincent execute result for testing"""
    def create_result(completed=True, required_outputs=None, outputs=None, tools=None, failure_step=None):
        result = Mock()
        result.completed = completed
        result.required_outputs = required_outputs or []
        result.outputs = outputs or []
        result.tools = tools or []
        result.failure_step = failure_step
        return result
    return create_result