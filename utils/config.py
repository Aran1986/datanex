# Location: datanex/utils/config.py

from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "BigData Analysis Service"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://admin:admin123@localhost:5432/bigdata"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # MinIO
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin123"
    MINIO_BUCKET: str = "bigdata-files"
    MINIO_SECURE: bool = False
    
    # AI Providers
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    
    # Blockchain
    INFURA_API_KEY: str = ""
    ALCHEMY_API_KEY: str = ""
    ETHEREUM_RPC: str = "https://mainnet.infura.io/v3/"
    
    # File Processing
    MAX_UPLOAD_SIZE: int = 500 * 1024 * 1024  # 500MB
    ALLOWED_EXTENSIONS: list = [
        "csv", "xlsx", "xls", "json", "xml", "parquet",
        "pdf", "docx", "txt", "html", "sql"
    ]
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()