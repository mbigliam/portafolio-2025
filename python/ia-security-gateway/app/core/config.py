"""
Configuration module for IA Security Gateway
Pydantic v2 compatible settings
"""
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Application settings and configuration"""

    # Server Configuration
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    DEBUG: bool = False

    # Ollama Local LLM Configuration
    OLLAMA_BASE_URL: str = "http://127.0.0.1:11434"
    OLLAMA_URL: str = "http://127.0.0.1:11434"
    OLLAMA_MODEL: str = "mistral"
    OLLAMA_TIMEOUT: int = 30

    # Gemini Configuration (Fallback - Optional)
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-pro"

    # Traffic Control & Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 900  # 15 minutes in seconds
    MAX_PAYLOAD_SIZE: int = 10_485_760  # 10MB

    # Compliance & Regulatory
    GDPR_ENABLED: bool = True
    HIPAA_ENABLED: bool = True
    PCI_DSS_ENABLED: bool = True
    LOG_SENSITIVE_DATA: bool = False
    RETENTION_DAYS: int = 90

    # CORS Configuration
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000"
    ]

    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/gateway.log"

    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()
