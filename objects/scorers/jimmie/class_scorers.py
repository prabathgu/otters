import weave
from weave import Scorer
from openai import OpenAI
import numpy as np
from typing import Dict, Any, List
from pydantic import Field

class MemorySimilarityScorer(Scorer):
    """Scores the similarity between generated and expected memories using embeddings"""
    
    threshold: float = Field(default=0.7, description="Similarity threshold for memory comparison")
    embedding_model: str = Field(default="text-embedding-ada-002", description="OpenAI embedding model to use")
    client: OpenAI = Field(default_factory=OpenAI, description="OpenAI client instance")

    @weave.op
    def get_embedding(self, text: str) -> List[float]:
        """Get embeddings for a text string"""
        return self.client.embeddings.create(
            input=text,
            model=self.embedding_model
        ).data[0].embedding

    @weave.op
    def calculate_similarity(self, emb1: List[float], emb2: List[float]) -> float:
        """Calculate cosine similarity between two embeddings"""
        return float(np.dot(emb1, emb2) / (
            np.linalg.norm(emb1) * np.linalg.norm(emb2)
        ))

    @weave.op
    def score(self, target: Dict[str, Any], output: List[str]) -> Dict[str, Any]:
        """Score the similarity between generated and expected memories"""
        # Get expected memories from target
        expected_memories = target.get('expected_memories', [])
        
        # Join the memories into strings
        generated_memories = ' '.join(output)
        expected_memories_text = ' '.join(expected_memories)
        
        # Get embeddings
        generated_embedding = self.get_embedding(generated_memories)
        expected_embedding = self.get_embedding(expected_memories_text)
        
        # Calculate similarity
        similarity = self.calculate_similarity(generated_embedding, expected_embedding)
        
        return {
            "similarity_score": similarity,
            "is_similar": similarity >= self.threshold
        } 