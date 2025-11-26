from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application configuration settings."""
    
    app_title: str = "Collaborative Code Editor"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Database settings
    database_url: str = "sqlite:///./test.db"
    
    # CORS settings
    allowed_origins: list = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000"
    ]
    
    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
