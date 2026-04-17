"""
GigaChat реализация LLM-судьи (заглушка)
"""

from typing import Tuple
from src.services.judge_constants import is_successful_response


async def evaluate(prompt: str, response: str) -> Tuple[bool, float, float]:
    """Заглушка для GigaChat"""
    if is_successful_response(response):
        return True, 0.7, 0.8
    return False, 0.5, 0.3