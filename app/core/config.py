from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    # Database Configuration
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:root@localhost:5432/wealth"
    )
    database_test_url: str = "postgresql://postgres:password@localhost:5432/marketpro_test_db"
    
    # Security
    secret_key: str = os.getenv(
        "SECRET_KEY",
        "your-secret-key-here-make-it-long-and-random"
    )
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # Email Configuration (Gmail)
    smtp_host: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port: int = int(os.getenv("SMTP_PORT", 587))
    smtp_user: str = os.getenv("SMTP_USER", "your-gmail@gmail.com")
    smtp_password: str = os.getenv("SMTP_PASSWORD", "your-gmail-app-password")
    
    # Redis Configuration
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # AWS Configuration
    aws_access_key_id: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region: str = os.getenv("AWS_REGION", "us-east-1")
    aws_s3_bucket: str = os.getenv("AWS_S3_BUCKET", "marketpro-uploads")
    
    # Stripe Configuration
    stripe_secret_key: Optional[str] = os.getenv("STRIPE_SECRET_KEY")
    stripe_publishable_key: Optional[str] = os.getenv("STRIPE_PUBLISHABLE_KEY")
    stripe_webhook_secret: Optional[str] = os.getenv("STRIPE_WEBHOOK_SECRET")
    
    # Angel One API Configuration
    angel_api_key: Optional[str] = os.getenv("ANGEL_API_KEY")
    angel_client_id: Optional[str] = os.getenv("ANGEL_CLIENT_ID")
    angel_refresh_token: Optional[str] = os.getenv("ANGEL_REFRESH_TOKEN")
    angel_feed_token: Optional[str] = os.getenv("ANGEL_FEED_TOKEN")
    angel_totp_secret: Optional[str] = os.getenv("ANGEL_TOTP_SECRET")
    angel_mpin: Optional[str] = os.getenv("ANGEL_MPIN")
    
    # Application Settings
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    environment: str = os.getenv("ENVIRONMENT", "production")
    api_v1_prefix: str = "/api/v1"
    project_name: str = "Wealth Genius Trading Education Platform"
    
    # CORS Origins - Default to production frontend. Override via env if needed.
    # Avoid using List[str] at class level with env parsing to prevent pydantic JSON errors.
    cors_origins: List[str] = [
        "https://wealth-frontend-three.vercel.app",  # Production frontend
    ]

    def __init__(self, **data):
        super().__init__(**data)
        # Parse CORS_ORIGINS from env after pydantic initialization
        cors_env = os.getenv("CORS_ORIGINS", "").strip()
        if cors_env and cors_env != "CORS_ORIGINS":  # Skip if env var is empty or unset placeholder
            try:
                # Try JSON array format first: ["https://a.com", "https://b.com"]
                import json
                self.cors_origins = json.loads(cors_env)
            except (json.JSONDecodeError, ValueError):
                # Fall back to comma-separated: "https://a.com,https://b.com"
                self.cors_origins = [o.strip() for o in cors_env.split(",") if o.strip()]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
