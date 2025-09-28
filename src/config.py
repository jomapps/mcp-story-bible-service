"""
Configuration settings for MCP Story Bible Service
"""

from pydantic import BaseSettings, Field
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Service Configuration
    HOST: str = Field(default="0.0.0.0", description="Host to bind the service")
    PORT: int = Field(default=8015, description="Port to run the service")
    ENVIRONMENT: str = Field(default="development", description="Environment (development/production)")
    
    # Database Configuration
    DATABASE_URL: str = Field(
        default="postgresql://story_bible_user:story_bible_password@localhost:5432/story_bible_db",
        description="PostgreSQL database URL"
    )
    
    # Brain Service Configuration
    BRAIN_SERVICE_URL: str = Field(
        default="http://localhost:8002",
        description="MCP Brain Service base URL"
    )
    BRAIN_SERVICE_WS_URL: str = Field(
        default="ws://localhost:8002/mcp",
        description="MCP Brain Service WebSocket URL"
    )
    
    # Authentication
    API_KEY_SECRET: str = Field(default="dev-secret-key", description="API key secret")
    JWT_SECRET_KEY: str = Field(default="dev-jwt-secret", description="JWT secret key")
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    JWT_EXPIRE_MINUTES: int = Field(default=60, description="JWT expiration time in minutes")
    
    # AI Configuration
    OPENAI_API_KEY: Optional[str] = Field(default=None, description="OpenAI API key")
    OPENAI_MODEL: str = Field(default="gpt-4", description="OpenAI model to use")
    
    # Logging Configuration
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FILE: Optional[str] = Field(default="logs/story_bible_service.log", description="Log file path")
    
    # Monitoring
    ENABLE_METRICS: bool = Field(default=True, description="Enable Prometheus metrics")
    METRICS_PORT: int = Field(default=9015, description="Metrics port")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()