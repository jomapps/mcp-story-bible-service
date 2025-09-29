"""Client wrapper for interacting with the MCP Brain Service."""

import asyncio
import json
import logging
import uuid
from typing import Any, Dict, Optional

import httpx
import websockets

from ..utils.exceptions import BrainServiceException


logger = logging.getLogger(__name__)


class BrainServiceClient:
    def __init__(self, base_url: str, ws_url: str, timeout: float) -> None:
        self._base_url = base_url.rstrip("/")
        self._ws_url = ws_url
        self._timeout = timeout
        self._http = httpx.AsyncClient(
            base_url=self._base_url,
            timeout=httpx.Timeout(timeout),
        )
        self._ws: Optional[websockets.WebSocketClientProtocol] = None
        self._ws_lock = asyncio.Lock()

    async def connect(self) -> None:
        try:
            self._ws = await websockets.connect(self._ws_url, open_timeout=self._timeout)
            logger.info("Connected to Brain Service WebSocket")
        except Exception as exc:
            self._ws = None
            logger.warning("WebSocket connection to Brain Service unavailable: %s", exc)

    async def disconnect(self) -> None:
        if self._ws is not None:
            try:
                await self._ws.close()
            except Exception:  # noqa: BLE001
                logger.debug("Failed to close Brain Service WebSocket cleanly")
        await self._http.aclose()

    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        if self._ws is not None:
            return await self._call_tool_ws(name, arguments)
        return await self._call_tool_http(name, arguments)

    async def _call_tool_ws(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        assert self._ws is not None
        request_id = str(uuid.uuid4())
        payload = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": "call_tool",
            "params": {"name": name, "arguments": arguments},
        }

        async with self._ws_lock:
            try:
                await self._ws.send(json.dumps(payload))
                response_raw = await asyncio.wait_for(self._ws.recv(), timeout=self._timeout)
            except Exception as exc:
                raise BrainServiceException(f"Brain Service WebSocket call failed: {exc}") from exc

        response = json.loads(response_raw)
        if "error" in response:
            raise BrainServiceException(response["error"].get("message", "Unknown Brain Service error"))
        return response.get("result", {})

    async def _call_tool_http(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        try:
            resp = await self._http.post(f"/tools/{name}", json=arguments)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPError as exc:
            raise BrainServiceException(f"Brain Service HTTP call failed: {exc}") from exc
