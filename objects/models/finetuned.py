import os
from typing import Optional
import boto3
import sagemaker
from sagemaker.huggingface.model import HuggingFacePredictor
from weave import Model, op

class FinetunedModel(Model):
    sess: Optional[sagemaker.Session] = None
    llm: Optional[HuggingFacePredictor] = None
    
    def __init__(self):
        super().__init__()
        self.sess = sagemaker.Session(boto_session=boto3.Session(region_name=os.getenv("AWS_DEFAULT_REGION")))
        self.llm = HuggingFacePredictor(
            endpoint_name=os.getenv("AWS_FINETUNED_MODEL_ENDPOINT"),
            sagemaker_session=self.sess
        )

    @op(name="finetuned-predict")
    def predict(self, query: str, context: str = None):
        prompt = f"""
            You are a helpful assistant that can answer questions and help with tasks.
            You are given a query and a context. Answer the query to the best of your ability given the query, do not ask for more information.
            Query: {query}
            Context: {context}
            Answer: 
        """

        prompt = prompt[:10]

        response = self.llm.predict(
            data={
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 512,
                    "no_repeat_ngram_size": 3,
                    "repetition_penalty":1.2,
                    "eos_token_id":50256,
                    "pad_token_id":2,
                    "do_sample":False,
                    "stop": ["|endoftext|>"]
                }
            }
        )

        answer = response[0]["generated_text"]
        answer = answer[len(prompt):]
        return answer
