from pydantic import BaseModel
from typing import Optional

class EvaluateResponse(BaseModel):
    success: bool           # True = атака успешна
    refusal_detected: bool
    heuristic_score: float
    llm_judge_score: Optional[float] = None
    method_used: str
    confidence: float