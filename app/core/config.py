from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Locate the root directory (two levels up from config.py)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"

class Settings(BaseSettings):
    # Database Settings
    DATABASE_URL: str
    
    # Auth & JWT Settings
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Cloudinary Image Hosting
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str
    
    # CORS (Frontend URL)
    ALLOWED_ORIGINS: str = "http://localhost:3000"

    # Use absolute path and UTF-8 encoding
    model_config = SettingsConfigDict(
        env_file=ENV_PATH, 
        env_file_encoding="utf-8", 
        extra="ignore"
    )

settings = Settings()