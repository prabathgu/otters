import boto3
import json
import dotenv
import os

# Tests:
#import os; os.environ['AWS_ACCESS_KEY_ID'] = 'xyz'
#model_id = "us.anthropic.claude-3-17-sonnet-20250219-v1:0"

dotenv.load_dotenv()


model_id = "us.anthropic.claude-3-7-sonnet-20250219-v1:0" # TEST MODEL IDs here
try:
    bedrock_client: boto3.client = boto3.client('bedrock-runtime', region_name=os.getenv("AWS_DEFAULT_REGION"))
except Exception as e:
    print(f"FAILED: You likely are missing API keys or the keys are incorrect. Please try again or request assistance: {e}")
    exit(1)

claude_messages = []
system_message = "Do some work!"
claude_messages.append({
    "role": "user",
    "content": "What is the capital of France?"
})

# Prepare the request body for Bedrock
request_body = {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 4000,
    "temperature": 0.7,
    "system": system_message,
    "messages": claude_messages
}

try:
    # Make the Bedrock API call
    response = bedrock_client.invoke_model(
        modelId=model_id,
        body=json.dumps(request_body)
    )

    body_unparsed = response['body'].read()
    response_body = json.loads(body_unparsed)

except Exception as e:
    print(f"FAILED: You likely are using an incorrect model ID. Please check the model ID and try again: {e}")
    exit(1)

print("If the following response is not empty, you are good to go!\n")
print(response_body)