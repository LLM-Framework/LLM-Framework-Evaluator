from pydantic import BaseModel
from enum import Enum

class EvaluationMethod(str, Enum):
    HEURISTIC = "heuristic"
    LLM_JUDGE = "llm_judge"
    HYBRID = "hybrid"

class EvaluateRequest(BaseModel):
    prompt: str
    response: str
    method: EvaluationMethod = EvaluationMethod.HYBRID