from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    evaluator_host: str = "0.0.0.0"
    evaluator_port: int = 8003
    debug: bool = True
    judge_provider: str = "mock"
    judge_api_key: str = ""

    class Config:
        env_file = ".env"


settings = Settings()