from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    evaluator_host: str = "0.0.0.0"
    evaluator_port: int = 8003
    debug: bool = True
    judge_provider: str = "yandex"
    judge_api_key: str = ""  # Можно использовать ключ из LLM Proxy
    judge_folder_id: str = ""
    judge_model: str = "yandexgpt-lite"

    class Config:
        env_file = ".env"


settings = Settings()