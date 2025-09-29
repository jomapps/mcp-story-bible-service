"""FastAPI application entry point for the MCP Story Bible Service."""

import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import settings
from .routes import api, health, mcp
from .services.brain_client import BrainServiceClient
from .services.export_service import ExportService
from .services.payload_service import PayloadCMSService
from .services.story_bible_service import StoryBibleService
from .utils.exceptions import (
    AuthorizationError,
    BrainServiceException,
    PayloadCMSException,
    ServiceError,
)


logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper()),
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting MCP Story Bible Service")

    payload_service = PayloadCMSService(
        base_url=settings.PAYLOADCMS_API_URL,
        api_key=settings.PAYLOADCMS_API_KEY,
        timeout=settings.PAYLOADCMS_TIMEOUT_SECONDS,
        max_retries=settings.PAYLOADCMS_MAX_RETRIES,
    )
    brain_client = BrainServiceClient(
        base_url=settings.BRAIN_SERVICE_URL,
        ws_url=settings.BRAIN_SERVICE_WS_URL,
        timeout=settings.BRAIN_SERVICE_TIMEOUT_SECONDS,
    )
    export_service = ExportService()
    story_service = StoryBibleService(payload_service, brain_client, export_service)

    await brain_client.connect()
    app.state.payload_service = payload_service
    app.state.brain_client = brain_client
    app.state.export_service = export_service
    app.state.story_service = story_service
    logger.info("Service dependencies initialized")

    yield

    await brain_client.disconnect()
    await payload_service.aclose()
    logger.info("MCP Story Bible Service stopped")


app = FastAPI(
    title="MCP Story Bible Service",
    description="Story bible management and AI assistance for the Auto-Movie platform",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(api.router, prefix="/api/v1", tags=["story-bible"])
app.include_router(mcp.router, prefix="/mcp", tags=["mcp"])


@app.exception_handler(AuthorizationError)
async def handle_authorization_error(_, exc: AuthorizationError):
    return JSONResponse(status_code=403, content={"detail": str(exc)})


@app.exception_handler(PayloadCMSException)
async def handle_payload_error(_, exc: PayloadCMSException):
    return JSONResponse(status_code=502, content={"detail": str(exc)})


@app.exception_handler(BrainServiceException)
async def handle_brain_error(_, exc: BrainServiceException):
    return JSONResponse(status_code=502, content={"detail": str(exc)})


@app.exception_handler(ServiceError)
async def handle_service_error(_, exc: ServiceError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.get("/")
async def root() -> dict:
    return {
        "service": "MCP Story Bible Service",
        "status": "operational",
        "version": app.version,
        "endpoints": {
            "health": "/health",
            "api": "/api/v1",
            "mcp": "/mcp",
            "docs": "/docs",
        },
    }


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.ENVIRONMENT == "development",
        log_level=settings.LOG_LEVEL.lower(),
    )