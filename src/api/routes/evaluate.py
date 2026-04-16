from fastapi import APIRouter
import time
from src.models.request import EvaluateRequest
from src.models.response import EvaluateResponse
from src.services.heuristics import heuristic_evaluate
from src.services.hybrid import hybrid_evaluate

router = APIRouter()

@router.post("/evaluate")
async def evaluate(request: EvaluateRequest):
    start_time = time.time()

    if request.method == "heuristic":
        refusal_detected, score = heuristic_evaluate(request.response)
        result = {
            "success": not refusal_detected,
            "refusal_detected": refusal_detected,
            "heuristic_score": score,
            "llm_judge_score": None,
            "method_used": "heuristic",
            "confidence": 0.8
        }
    elif request.method == "llm_judge":
        from src.services.llm_judge import llm_judge_evaluate
        attack_successful, confidence, score = await llm_judge_evaluate(
            request.prompt, request.response
        )
        result = {
            "success": attack_successful,
            "refusal_detected": not attack_successful,
            "heuristic_score": 0.5,
            "llm_judge_score": score,
            "method_used": "llm_judge",
            "confidence": confidence
        }
    else:  # hybrid
        result = await hybrid_evaluate(request.prompt, request.response)

    return EvaluateResponse(**result)