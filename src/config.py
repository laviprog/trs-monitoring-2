from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or a .env file.
    """

    model_config = SettingsConfigDict(env_file=".env")

    LOG_LEVEL: str = "DEBUG"  # DEBUG | INFO | WARNING | ERROR | CRITICAL
    ENV: str = "dev"  # dev | prod
    TMP_DIR: str = "/tmp"  # Temporary directory

    # Transcription API
    TRANSCRIPTION_BASE_URL: str
    TRANSCRIPTION_USERNAME: str
    TRANSCRIPTION_PASSWORD: str

    # Backend API
    BACKEND_BASE_URL: str
    BACKEND_API_KEY: str


settings = Settings()
