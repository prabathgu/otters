import json
import os
import boto3
from weave import Scorer
import weave
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from utils.helpers import clean_claude_json


# Feel free to add more scorers here to help evaluate the model.
# For example, you could add a scorer to evaluate the model's ability to use tools,
# or to evaluate the model's ability to reason about the user's request.
# You could also add a scorer to evaluate the model's ability to handle errors,
# or to evaluate the model's ability to handle edge cases.
# You could also add a scorer to evaluate the model's ability to handle long requests,
# or to evaluate the model's ability to handle short requests.


#######################################################################
#### DO NOT MODIFY BELOW THIS LINE (Feel free to add more scorers) ####
#######################################################################
class Judgement(BaseModel):
    """Inner judgement object containing the evaluation details."""
    score: float = Field(..., ge=0.0, le=1.0, description="Quality score between 0.0 and 1.0")
    accuracy_score: float = Field(..., ge=0.0, le=1.0, description="Accuracy score between 0.0 and 1.0 based on how well the response matches the expected target")
    reasoning: str = Field(..., description="Explanation of the score")
    strengths: List[str] = Field(..., description="List of strengths identified")
    weaknesses: List[str] = Field(..., description="List of weaknesses identified")
class ResponseQualityEvaluation(BaseModel):
    """Top-level response quality evaluation format."""
    judgement: Judgement = Field(..., description="The evaluation judgement")
class ResponseQualityScorer(Scorer):
    """Evaluates the quality of an AI assistant's response using an LLM.
    Different response types (statement, answer, question, plan) are evaluated 
    using type-specific criteria.
    """
    model_id: str = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
    bedrock_client: boto3.client = boto3.client('bedrock-runtime', region_name=os.getenv("AWS_DEFAULT_REGION"))
    
    def __init__(self, model_id: str, column_map: dict, region_name: str = os.getenv("AWS_DEFAULT_REGION")):
        super().__init__(model_id=model_id, column_map=column_map)
        # Remove 'bedrock/' prefix if present
        if model_id.startswith('bedrock/'):
            self.model_id = model_id[8:]
        else:
            self.model_id = model_id

    @weave.op
    def _build_prompt(self, user_input: str, output: Dict[str, Any], target: str) -> tuple[str, str]:
        """Builds the evaluation prompt based on response type.
        
        Returns:
            A tuple containing the system prompt and the user message content.
        """
        if output is None:
            return None, None
        

        response_type = output.get('type', '')
        prompt_template = {
        'statement': """
1. Empathy: Does it show appropriate understanding and acknowledgment?
2. Relevance: Is the statement directly related to the user's input?
3. Tone: Is the tone appropriate for the context?
4. Natural Flow: Does it sound natural and conversational?""",
        
        'answer': """
1. Accuracy: Is the answer factually correct?
2. Completeness: Does it fully address the question?
3. Explanation Quality: Is the explanation clear and well-supported?
4. Conciseness: Is it appropriately detailed without being verbose?""",
        
        'question': """
1. Relevance: Is the clarifying question directly related to the user's request?
2. Necessity: Is the question truly needed to better understand the user's needs?
3. Clarity: Is the question clear and easy to understand?
4. Purpose: Is the reason for asking the question well justified?""",
        
        'plan': """
1. Completeness: Does it include all necessary steps?
2. Tool Usage: Are the selected tools appropriate?
3. Step Sequence: Is the order of steps logical?
4. Efficiency: Is it the most efficient approach?"""
        }

        criteria = prompt_template.get(response_type, "")
        
        system_prompt = f"""You are an AI assistant quality evaluator.
Evaluate the AI assistant's {response_type} response to the user's request based on the provided criteria and context.
The user's request was: {user_input}
The expected target output (if available) is: {target}

Consider these specific criteria for a {response_type} response:
```
{criteria}
```

Provide two separate scores:
1. **Quality Score (0.0-1.0)**: Evaluate the overall quality based on the criteria above
2. **Accuracy Score (0.0-1.0)**: Evaluate how accurately the response matches the expected target answer. As long as the correct answer is provided, the accuracy score should be 1.0. If no target is provided or the target is not applicable, use 0.0 as a failure score. Precision errors are completely accetable.

The user will provide the AI assistant's actual response.
Provide your evaluation in JSON format:
{{
    "judgement": {{
        "score": <float between 0.0 and 1.0>,
        "accuracy_score": <float between 0.0 and 1.0>,
        "reasoning": <string explaining both scores>,
        "strengths": [<list of strengths>],
        "weaknesses": [<list of weaknesses>]
    }}
}}"""

        output_to_include = output.copy()
        if 'process' in output_to_include and 'steps_taken' in output_to_include['process']:
            for step in output_to_include['process']['steps_taken']:
                if 'output' in step:
                    del step['output']
        user_message_content = json.dumps(output_to_include, indent=2)
        
        return system_prompt, user_message_content

    @weave.op
    def score(self, output: Dict[str, Any], input: str, target: str) -> Dict[str, Any]:
        """
        Score the quality of the assistant's response.
        
        Args:
            output: The assistant's response dictionary
            input: The user's input text
        
        Returns:
            Dictionary containing quality metrics including score, reasoning, 
            strengths and weaknesses
        """
        sys_prompt, user_message_content = self._build_prompt(input, output, target)

        if output.get('type') not in output and not output.get('type') == "answer":
            return {
                'quality_score': 0.0,
                'accuracy_score': 0.0,
                'reasoning': f'Invalid response type: {output.get("type"), "No Type Provided"}',
                'strengths': [],
                'weaknesses': ['Invalid response type']
            }

        try:
            # Prepare the request body for Bedrock
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4000,
                "temperature": 0.3,
                "system": sys_prompt,
                "messages": [
                    {"role": "user", "content": user_message_content}
                ]
            }

            # Make the Bedrock API call
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            

            body_unparsed = response['body'].read()
            response_body = json.loads(body_unparsed)
            content = response_body['content'][0]['text']
            # Clean the content by removing markdown code block markers and extracting JSON
            cleaned_content = clean_claude_json(content)
            
            # Parse response using Pydantic model
            evaluation = ResponseQualityEvaluation.model_validate_json(cleaned_content)
            
            return {
                'quality_score': evaluation.judgement.score,
                'accuracy_score': evaluation.judgement.accuracy_score,
                'reasoning': evaluation.judgement.reasoning,
                'strengths': evaluation.judgement.strengths,
                'weaknesses': evaluation.judgement.weaknesses
            }
            
        except Exception as e:
            return {
                'quality_score': 0.0,
                'accuracy_score': 0.0,
                'reasoning': f'Error during evaluation: {str(e)}',
                'strengths': [],
                'weaknesses': ['Evaluation failed']
            }

    def summarize(self, score_rows: list) -> dict:
        """
        Summarize scores across all evaluated responses.
        
        Args:
            score_rows: List of score dictionaries from each evaluation
            
        Returns:
            Dictionary with aggregated metrics
        """
        if not score_rows:
            return {
                'mean_quality_score': 0.0,
                'mean_accuracy_score': 0.0,
                'total_strengths': 0,
                'total_weaknesses': 0
            }
            
        quality_scores = [row['quality_score'] for row in score_rows]
        accuracy_scores = [row['accuracy_score'] for row in score_rows]
        total_strengths = sum(len(row['strengths']) for row in score_rows)
        total_weaknesses = sum(len(row['weaknesses']) for row in score_rows)
        
        return {
            'mean_quality_score': sum(quality_scores) / len(quality_scores),
            'mean_accuracy_score': sum(accuracy_scores) / len(accuracy_scores),
            'total_strengths': total_strengths,
            'total_weaknesses': total_weaknesses
        } 