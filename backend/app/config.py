from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/v1"
    PROJECT_NAME: str = "German Simplification API"
    VERSION: str = "1.0.0"
    
    # Database Configuration
    DATABASE_URL: str = "postgresql://user:password@postgres:5432/simple_german"
    
    # Redis Configuration
    REDIS_URL: str = "redis://redis:6379/0"
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0
    REDIS_MAX_CONNECTIONS: int = 20
    REDIS_CONNECTION_TIMEOUT: int = 5
    REDIS_SOCKET_TIMEOUT: int = 5
    
    # Security Configuration
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001"]
    
    # Hugging Face Configuration
    HF_API_TOKEN: Optional[str] = None
    MODEL_NAME: str = "DEplain/mt5-simple-german-corpus"
    MODEL_VERSION: str = "mt5-v1.0"
    
    # AWS S3 Configuration
    AWS_S3_ENDPOINT_URL: Optional[str] = None
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_S3_BUCKET: str = "simple-german-cache"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()
