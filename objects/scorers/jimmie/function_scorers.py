import weave
from typing import Dict, Any, List
import json
from openai import OpenAI
import numpy as np

@weave.op()
def memory_creation_scorer(target: object, output: List[str]) -> bool:
    """
    Scores whether Jimmie correctly identifies when to create memories.
    Returns True if Jimmie made the correct decision about creating memories.
    
    A correct decision means:
    - Created memories when expected_memories is not empty
    - Did not create memories when expected_memories is empty
    """
    expected_memories = target.get('expected_memories', [])
    
    # If we expect memories, check if any were created
    if expected_memories:
        return len(output) > 0
    
    # If we don't expect memories, check that none were created
    return len(output) == 0