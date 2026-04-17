"""
LLM-as-a-Judge модуль для оценки успешности промпт-инъекций
"""

from typing import Tuple
from src.config import settings
from src.services import yandex_judge, gigachat_judge
from src.services.judge_constants import is_successful_response, DEFAULT_CONFIDENCE


async def llm_judge_evaluate(prompt: str, response: str) -> Tuple[bool, float, float]:
    """
    Оценивает ответ через LLM.

    Returns:
        Tuple[bool, float, float]: (attack_successful, confidence, score)
    """
    provider = settings.judge_provider

    if provider == "yandex":
        return await yandex_judge.evaluate(prompt, response)
    elif provider == "gigachat":
        return await gigachat_judge.evaluate(prompt, response)
    else:
        return _fallback(response)


def _fallback(response: str) -> Tuple[bool, float, float]:
    """Эвристическая оценка без вызова API"""
    if is_successful_response(response):
        return True, 0.8, 0.9
    return False, DEFAULT_CONFIDENCE, 0.3


def get_judge_status() -> dict:
    """Возвращает статус конфигурации судьи"""
    from src.services import yandex_judge

    return {
        "provider": settings.judge_provider,
        "yandex_configured": yandex_judge.is_configured(),
        "model": settings.judge_model if settings.judge_provider == "yandex" else None
    }