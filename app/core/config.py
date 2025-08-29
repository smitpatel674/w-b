from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    # Database Configuration
    database_url: str = "postgresql://postgres:root@localhost:5432/wealth"
    database_test_url: str = "postgresql://postgres:password@localhost:5432/marketpro_test_db"
    
    # Security
    secret_key: str = "your-secret-key-here-make-it-long-and-random"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # Email Configuration (Gmail)
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = "your-gmail@gmail.com"
    smtp_password: str = "your-gmail-app-password"
    
    # Redis Configuration
    redis_url: str = "redis://localhost:6379"
    
    # AWS Configuration
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_region: str = "us-east-1"
    aws_s3_bucket: str = "marketpro-uploads"
    
    # Stripe Configuration
    stripe_secret_key: Optional[str] = None
    stripe_publishable_key: Optional[str] = None
    stripe_webhook_secret: Optional[str] = None
    
    # Application Settings
    debug: bool = True
    environment: str = "development"
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    api_v1_prefix: str = "/api/v1"
    project_name: str = "MarketPro Trading Education Platform"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
