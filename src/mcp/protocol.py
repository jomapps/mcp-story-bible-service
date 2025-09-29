"""Minimal JSON-RPC like protocol helpers for MCP WebSocket."""

from typing import Any, Dict


def build_success_response(request_id: Any, result: Any) -> Dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def build_error_response(request_id: Any, message: str) -> Dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "error": {"message": message}}
