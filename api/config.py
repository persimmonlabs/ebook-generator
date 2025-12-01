"""Configuration settings for the Ebook Generator API."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # OpenRouter API
    OPENROUTER_API_KEY: str

    # Supabase Configuration
    SUPABASE_URL: str
    SUPABASE_SERVICE_ROLE_KEY: str
    SUPABASE_JWT_SECRET: str

    # CORS - Comma-separated allowed origins
    ALLOWED_ORIGINS: str = "http://localhost:3000"

    # Server (Railway sets PORT automatically)
    PORT: int = 8000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
