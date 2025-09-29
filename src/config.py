"""Configuration settings for MCP Story Bible Service."""

from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    HOST: str = Field(default="0.0.0.0", description="Host to bind the service")
    PORT: int = Field(default=8015, description="Port to run the service")
    ENVIRONMENT: str = Field(default="development", description="Deployment environment")

    # PayloadCMS Integration
    PAYLOADCMS_API_URL: str = Field(
        default="http://localhost:3010",
        description="PayloadCMS API endpoint exposed by Auto-Movie App",
    )
    PAYLOADCMS_API_KEY: Optional[str] = Field(
        default=None,
        description="Service-to-service API key for PayloadCMS (Auto-Movie App)",
    )
    PAYLOADCMS_TIMEOUT_SECONDS: float = Field(
        default=30.0,
        description="HTTP timeout when communicating with PayloadCMS",
    )
    PAYLOADCMS_MAX_RETRIES: int = Field(
        default=3,
        description="Maximum number of retries for PayloadCMS operations",
    )

    # Brain Service Configuration
    BRAIN_SERVICE_URL: str = Field(
        default="http://localhost:8002",
        description="MCP Brain Service base URL",
    )
    BRAIN_SERVICE_WS_URL: str = Field(
        default="ws://localhost:8002/mcp",
        description="Brain Service MCP WebSocket URL",
    )
    BRAIN_SERVICE_TIMEOUT_SECONDS: float = Field(
        default=30.0,
        description="Timeout for Brain Service requests",
    )

    # Authentication
    ALLOWED_ORIGINS: List[str] = Field(
        default_factory=lambda: [
            "http://localhost:3010",
            "https://auto-movie.ngrok.pro",
            "https://auto-movie.ft.tc",
        ],
        description="Allowed CORS origins",
    )

    # Logging Configuration
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FILE: Optional[str] = Field(default=None, description="Optional log file path")

    # Monitoring
    ENABLE_METRICS: bool = Field(default=True, description="Enable Prometheus metrics")
    METRICS_PORT: int = Field(default=9015, description="Prometheus metrics port")

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()