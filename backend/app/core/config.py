from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Groq
    groq_api_key: str
    groq_model: str = "llama-3.1-8b-instant"
    groq_chat_max_tokens: int = 512
    groq_chat_temperature: float = 0.7
    groq_insight_max_tokens: int = 60
    groq_insight_temperature: float = 0.1

    # CORS
    cors_origins: list[str] = ["http://localhost:5173"]

    # App
    app_title: str = "Chat Assistant API"
    app_version: str = "1.0.0"

    # Logging
    log_level: str = "INFO"
    log_to_file: bool = True
    log_file_path: str = "logs/app.log"
    log_max_bytes: int = 5 * 1024 * 1024   # 5 MB per file
    log_backup_count: int = 3               # keep 3 rotated files


# Single shared instance imported across the app
settings = Settings()
