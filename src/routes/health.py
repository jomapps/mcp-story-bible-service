"""Health endpoints."""

import time

from fastapi import APIRouter

router = APIRouter()


@router.get("/live")
async def live() -> dict:
    return {"status": "ok", "timestamp": int(time.time())}


@router.get("/ready")
async def ready() -> dict:
    return {"status": "ready", "timestamp": int(time.time())}
