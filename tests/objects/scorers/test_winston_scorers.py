import unittest
from unittest.mock import patch
from objects.scorers.winston.function_scorers import (
    ResponseTypeScorer,
    ToolUsageScorer, 
    ResponseStructureScorer
)

class TestWinstonScorers(unittest.TestCase):
    def setUp(self):
        self.response_type_scorer = ResponseTypeScorer()
        self.tool_usage_scorer = ToolUsageScorer()
        self.response_structure_scorer = ResponseStructureScorer()

    def test_response_type_scorer_basic(self):
        """Test basic functionality of response type scorer"""
        target = {"response_type_scorer": "plan"}
        output = {"type": "plan"}
        self.assertTrue(ResponseTypeScorer().score(target, output))

    def test_response_type_scorer_mismatch(self):
        """Test type mismatch cases"""
        test_cases = [
            # Type mismatch
            ({"response_type_scorer": "question"}, {"type": "plan"}, False),
            # Missing type in output
            ({"response_type_scorer": "plan"}, {}, False),
            # None type in output
            ({"response_type_scorer": "plan"}, {"type": None}, False),
            # Empty string type
            ({"response_type_scorer": ""}, {"type": ""}, True),
        ]
        
        for target, output, expected in test_cases:
            with self.subTest(target=target, output=output):
                self.assertEqual(ResponseTypeScorer().score(target, output), expected)

    @patch('utils.helpers.load_tools')
    def test_tool_usage_scorer_basic(self, mock_load_tools):
        """Test basic functionality of tool usage scorer"""
        mock_load_tools.return_value = [
            {"function": {"name": "web-search_web"}},
            {"function": {"name": "chat_completion-generate_response"}}
        ]

        target = {
            "tool_usage_scorer": ["web-search_web", "chat_completion-generate_response"]
        }
        output = {
            "content": {
                "steps": [
                    {"tool": "web-search_web", "input": "query"},
                    {"tool": "chat_completion-generate_response", "input": "text"}
                ]
            }
        }
        result = ToolUsageScorer().score(target, output)
        self.assertEqual(
            result,
            {
                "used_expected_tools": True,
                "missing_tools": [],
                "additional_tools": [],
                "all_tools_valid": False,
                "invalid_tools": ["chat_completion-generate_response"],
                "valid_inputs": True,
                "input_errors": []
            }
        )

    @patch('utils.helpers.load_tools')
    def test_tool_usage_scorer_edge_cases(self, mock_load_tools):
        """Test edge cases for tool usage scorer"""
        mock_load_tools.return_value = [
            {"function": {"name": "web-search_web"}},
            {"function": {"name": "chat_completion-generate_response"}}
        ]

        test_cases = [
            # Empty required tools list - all tools used will be considered additional
            (
                {"tool_usage_scorer": {}}, 
                {"content": {"steps": [{"tool": "web-search_web"}]}},
                {
                    "used_expected_tools": True,
                    "missing_tools": [],
                    "additional_tools": ["web-search_web"],
                    "all_tools_valid": True,
                    "invalid_tools": [],
                    "valid_inputs": False,
                    "input_errors": ["web-search_web: Missing required parameter 'query'"]
                }
            ),
            # No tool_usage_scorer in target - should behave same as empty list
            (
                {}, 
                {"content": {"steps": [{"tool": "web-search_web"}]}},
                {
                    "used_expected_tools": True,
                    "missing_tools": [],
                    "additional_tools": ["web-search_web"],
                    "all_tools_valid": True,
                    "invalid_tools": [],
                    "valid_inputs": False,
                    "input_errors": ["web-search_web: Missing required parameter 'query'"]
                }
            ),
            # Invalid output structure
            (
                {"tool_usage_scorer": ["web-search_web"]}, 
                {"invalid": "structure"},
                {
                    "used_expected_tools": False,
                    "missing_tools": ["web-search_web"],
                    "additional_tools": [],
                    "all_tools_valid": True,
                    "invalid_tools": [],
                    "valid_inputs": True,
                    "input_errors": []
                }
            ),
            # Missing steps in content
            (
                {"tool_usage_scorer": ["web-search_web"]}, 
                {"content": {}},
                {
                    "used_expected_tools": False,
                    "missing_tools": ["web-search_web"],
                    "additional_tools": [],
                    "all_tools_valid": True,
                    "invalid_tools": [],
                    "valid_inputs": True,
                    "input_errors": []
                }
            ),
            # None steps in content
            (
                {"tool_usage_scorer": ["web-search_web"]}, 
                {"content": {"steps": None}},
                {
                    "used_expected_tools": False,
                    "missing_tools": ["web-search_web"],
                    "additional_tools": [],
                    "all_tools_valid": True,
                    "invalid_tools": [],
                    "valid_inputs": True,
                    "input_errors": []
                }
            ),
            # Missing expected tools but has additional tools
            (
                {"tool_usage_scorer": ["expected-tool"]},
                {"content": {"steps": [{"tool": "additional-tool"}]}},
                {
                    "used_expected_tools": False,
                    "missing_tools": ["expected-tool"],
                    "additional_tools": ["additional-tool"],
                    "all_tools_valid": False,
                    "invalid_tools": ["additional-tool"],
                    "valid_inputs": True,
                    "input_errors": []
                }
            ),
        ]
        
        for target, output, expected in test_cases:
            with self.subTest(target=target, output=output):
                self.assertEqual(ToolUsageScorer().score(target, output), expected)

    @patch('utils.helpers.load_tools')
    def test_tool_usage_scorer_with_validation(self, mock_load_tools):
        """Test tool usage scorer with tool validation"""
        mock_load_tools.return_value = [
            {"function": {"name": "web-search_web"}},
            {"function": {"name": "chat_completion-generate_response"}}
        ]

        target = {
            "tool_usage_scorer": ["web-search_web"]
        }
        output = {
            "content": {
                "steps": [
                    {"tool": "web-search_web"},
                    {"tool": "nonexistent-tool"}
                ]
            }
        }
        result = ToolUsageScorer().score(target, output)
        self.assertEqual(
            result,
            {
                "used_expected_tools": True,
                "missing_tools": [],
                "additional_tools": ["nonexistent-tool"],
                "all_tools_valid": False,
                "invalid_tools": ["nonexistent-tool"],
                "valid_inputs": False,
                "input_errors": ["web-search_web: Missing required parameter 'query'"]
            }
        )

    @patch('utils.helpers.load_tools')
    def test_tool_usage_scorer_all_valid_tools(self, mock_load_tools):
        """Test tool usage scorer with all valid tools"""
        mock_load_tools.return_value = [
            {
                "function": {
                    "name": "web-search_web",
                    "parameters": {
                        "properties": {
                            "query": {"type": "string"}
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "function": {
                    "name": "chat_completion-generate_response",
                    "parameters": {
                        "properties": {
                            "messages": {"type": "array"}
                        },
                        "required": ["messages"]
                    }
                }
            }
        ]

        target = {
            "tool_usage_scorer": ["web-search_web"]
        }
        output = {
            "content": {
                "steps": [
                    {"tool": "web-search_web"},
                    {"tool": "chat_completion-generate_response"}
                ]
            }
        }
        result = ToolUsageScorer().score(target, output)
        self.assertEqual(
            result,
            {
                "used_expected_tools": True,
                "missing_tools": [],
                "additional_tools": ["chat_completion-generate_response"],
                "all_tools_valid": False,
                "invalid_tools": ["chat_completion-generate_response"],
                "valid_inputs": False,
                "input_errors": ["web-search_web: Missing required parameter 'query'"]
            }
        )

    def test_response_type_scorer_none_output(self):
        """Test response type scorer with None output"""
        target = {"response_type_scorer": "answer"}
        result = ResponseTypeScorer().score(target, None)
        self.assertEqual(result, {'type': None})

    def test_response_structure_scorer_invalid_input(self):
        """Test response structure scorer with invalid input"""
        # Test with non-dict input
        result = ResponseStructureScorer().score("not a dict")
        self.assertEqual(result, {
            "valid_structure": False,
            "missing_properties": ["type", "content"],
            "invalid_properties": []
        })

        # Test with missing required fields
        result = ResponseStructureScorer().score({})
        self.assertEqual(result, {
            "valid_structure": False,
            "missing_properties": ["type", "content"],
            "invalid_properties": []
        })

    def test_response_structure_scorer_invalid_type(self):
        """Test response structure scorer with invalid response type"""
        output = {
            "type": "invalid_type",
            "content": {}
        }
        result = ResponseStructureScorer().score(output)
        self.assertEqual(result, {
            "valid_structure": False,
            "missing_properties": [],
            "invalid_properties": ["type"]
        })

    def test_response_structure_scorer_answer_type(self):
        """Test response structure scorer with answer type"""
        # Test valid answer structure
        valid_output = {
            "type": "answer",
            "content": {
                "message": "test message",
                "reason": "test reason"
            }
        }
        result = ResponseStructureScorer().score(valid_output)
        self.assertEqual(result, {
            "valid_structure": True,
            "missing_properties": [],
            "invalid_properties": []
        })

        # Test invalid property types
        invalid_output = {
            "type": "answer",
            "content": {
                "message": 123,  # Should be string
                "reason": "test reason"
            }
        }
        result = ResponseStructureScorer().score(invalid_output)
        self.assertEqual(result, {
            "valid_structure": False,
            "missing_properties": [],
            "invalid_properties": ["message"]
        })

    def test_response_structure_scorer_plan_type(self):
        """Test response structure scorer with plan type"""
        # Test valid plan structure
        valid_output = {
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
        }
        result = ResponseStructureScorer().score(valid_output)
        self.assertEqual(result, {
            "valid_structure": True,
            "missing_properties": [],
            "invalid_properties": []
        })

        # Test invalid step structure
        invalid_output = {
            "type": "plan",
            "content": {
                "steps": [
                    {
                        "step": "1",  # Should be int
                        "tool": 123,  # Should be string
                        "input": "test input",
                        "reason": ["invalid"],  # Should be string
                        "required_for_response": "true"  # Should be bool
                    }
                ]
            }
        }
        result = ResponseStructureScorer().score(invalid_output)
        self.assertEqual(result, {
            "valid_structure": False,
            "missing_properties": [],
            "invalid_properties": ["steps[0].step", "steps[0].tool", "steps[0].reason", "steps[0].required_for_response"]
        })

    def test_response_structure_scorer_question_type(self):
        """Test response structure scorer with question type"""
        # Test valid question structure
        valid_output = {
            "type": "question",
            "content": {
                "message": "test question?",
                "reason": "test reason"
            }
        }
        result = ResponseStructureScorer().score(valid_output)
        self.assertEqual(result, {
            "valid_structure": True,
            "missing_properties": [],
            "invalid_properties": []
        })

        # Test missing required properties
        invalid_output = {
            "type": "question",
            "content": {
                "message": "test question?"
                # missing reason
            }
        }
        result = ResponseStructureScorer().score(invalid_output)
        self.assertEqual(result, {
            "valid_structure": False,
            "missing_properties": ["reason"],
            "invalid_properties": []
        })

    def test_response_structure_scorer_plan_input_types(self):
        """Test response structure scorer with different plan input types"""
        # Test different valid input types
        valid_inputs = [
            "string input",
            {"key": "value"},
            None
        ]
        
        for input_value in valid_inputs:
            output = {
                "type": "plan",
                "content": {
                    "steps": [
                        {
                            "step": 1,
                            "tool": "test_tool",
                            "input": input_value,
                            "reason": "test reason",
                            "required_for_response": True
                        }
                    ]
                }
            }
            result = ResponseStructureScorer().score(output)
            self.assertEqual(result, {
                "valid_structure": True,
                "missing_properties": [],
                "invalid_properties": []
            })

        # Test invalid input type
        invalid_output = {
            "type": "plan",
            "content": {
                "steps": [
                    {
                        "step": 1,
                        "tool": "test_tool",
                        "input": 123,  # Number is not a valid input type
                        "reason": "test reason",
                        "required_for_response": True
                    }
                ]
            }
        }
        result = ResponseStructureScorer().score(invalid_output)
        self.assertEqual(result, {
            "valid_structure": False,
            "missing_properties": [],
            "invalid_properties": ["steps[0].input"]
        })

if __name__ == '__main__':
    unittest.main() 