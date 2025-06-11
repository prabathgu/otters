import boto3

import sagemaker
from sagemaker.huggingface.model import HuggingFacePredictor
from datetime import datetime
import os

# import dotenv
# dotenv.load_dotenv()

sess = sagemaker.Session(boto_session=boto3.Session(region_name=os.getenv("AWS_DEFAULT_REGION")))

llm = HuggingFacePredictor(
    endpoint_name=os.getenv("AWS_FINETUNED_MODEL_ENDPOINT"),
    sagemaker_session=sess
)

for i in range(10):
    print(llm.predict(
        data={
            "inputs": f"how do you spell out the number {i}?",
            "parameters": {
                "max_new_tokens": 256,
                "no_repeat_ngram_size": 3,
                "repetition_penalty":1.2,
                "eos_token_id":50256,
                "pad_token_id":2,
                "do_sample":False,
                "stop": ["|endoftext|>"]
            }
        }))
    print(datetime.now())
