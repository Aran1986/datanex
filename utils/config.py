from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # App
    APP_NAME: str = "DataNex"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://admin:admin123@localhost:5432/datanex"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # MinIO
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin123"
    MINIO_SECURE: bool = False
    MINIO_BUCKET: str = "datanex-files"
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # AI Providers (Optional)
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    
    # Blockchain (Optional)
    INFURA_API_KEY: str = ""
    ALCHEMY_API_KEY: str = ""
    ETHEREUM_RPC: str = "https://eth-mainnet.g.alchemy.com/v2/"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# Location: utils/config.py
