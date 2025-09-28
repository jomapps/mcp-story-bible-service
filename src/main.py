"""
MCP Story Bible Service - Main Application Entry Point

This service provides comprehensive story bible creation and management
for the AI Movie Generation Platform through the Model Context Protocol.
"""

import asyncio
import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import init_db
from .routes import health, api, mcp
from .services.brain_client import BrainServiceClient
from .services.story_bible_service import StoryBibleService


# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(settings.LOG_FILE) if settings.LOG_FILE else logging.NullHandler()
    ]
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler"""
    logger.info("Starting MCP Story Bible Service...")
    
    # Initialize database
    await init_db()
    logger.info("Database initialized")
    
    # Initialize Brain Service client
    brain_client = BrainServiceClient(
        base_url=settings.BRAIN_SERVICE_URL,
        ws_url=settings.BRAIN_SERVICE_WS_URL
    )
    await brain_client.connect()
    app.state.brain_client = brain_client
    logger.info("Brain service client connected")
    
    # Initialize Story Bible service
    story_service = StoryBibleService(brain_client)
    app.state.story_service = story_service
    logger.info("Story bible service initialized")
    
    logger.info(f"Service started on port {settings.PORT}")
    
    yield
    
    # Cleanup
    await brain_client.disconnect()
    logger.info("MCP Story Bible Service stopped")


# Create FastAPI app
app = FastAPI(
    title="MCP Story Bible Service",
    description="Comprehensive story bible creation and management service for AI Movie Generation Platform",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(api.router, prefix="/api/v1", tags=["api"])
app.include_router(mcp.router, prefix="/mcp", tags=["mcp"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "MCP Story Bible Service",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "api": "/api/v1",
            "mcp": "/mcp",
            "docs": "/docs"
        }
    }


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.ENVIRONMENT == "development",
        log_level=settings.LOG_LEVEL.lower()
    )