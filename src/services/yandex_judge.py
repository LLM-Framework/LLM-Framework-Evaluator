"""
YandexGPT реализация LLM-судьи
"""

import httpx
from typing import Tuple
from src.config import settings
from src.services.judge_constants import (
    JUDGE_PROMPT, is_successful_response, extract_json_from_text
)
# todo временно, потом будет задаваться динамически
YANDEX_API_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"


def is_configured() -> bool:
    """Проверяет, настроен ли YandexGPT"""
    return bool(settings.judge_api_key and settings.judge_folder_id)


async def evaluate(prompt: str, response: str) -> Tuple[bool, float, float]:
    """Вызов YandexGPT для оценки"""

    if not is_configured():
        return _fallback(response)

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                YANDEX_API_URL,
                headers=_get_headers(),
                json=_get_body(prompt, response)
            )

            if resp.status_code != 200:
                print(f"Yandex Judge error: {resp.text}")
                return _fallback(response)

            return _parse_response(resp.json(), response)

    except Exception as e:
        print(f"Exception in yandex_judge: {e}")
        return _fallback(response)


def _get_headers() -> dict:
    """Заголовки для запроса к YandexGPT"""
    return {
        "Authorization": f"Api-Key {settings.judge_api_key}",
        "Content-Type": "application/json"
    }


def _get_body(prompt: str, response: str) -> dict:
    """Тело запроса для YandexGPT"""
    judge_prompt = JUDGE_PROMPT.format(prompt=prompt, response=response)

    return {
        "modelUri": f"gpt://{settings.judge_folder_id}/{settings.judge_model}",
        "completionOptions": {
            "stream": False,
            "temperature": 0.0,
            "maxTokens": 200
        },
        "messages": [
            {"role": "user", "text": judge_prompt}
        ]
    }


def _parse_response(data: dict, response: str) -> Tuple[bool, float, float]:
    """Парсит ответ от YandexGPT"""
    result_text = data.get("result", {}).get("alternatives", [{}])[0].get("message", {}).get("text", "")

    parsed = extract_json_from_text(result_text)
    if parsed:
        attack_successful = parsed.get("attack_successful", False)
        confidence = parsed.get("confidence", 0.5)
        score = 1.0 if attack_successful else 0.0
        return attack_successful, confidence, score

    if "успеш" in result_text.lower() or "true" in result_text.lower():
        return True, 0.7, 0.8

    return _fallback(response)


def _fallback(response: str) -> Tuple[bool, float, float]:
    """Fallback на эвристику"""
    if is_successful_response(response):
        return True, 0.7, 0.8
    return False, 0.5, 0.3