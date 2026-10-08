from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "xigua-ai-workstation"
    app_env: str = "development"
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    frontend_port: int = 8080
    default_platform: str = "douyin"
    default_language: str = "zh-CN"
    secret_key: str = "change-me"

    class Config:
        env_file = ".env"


settings = Settings()
