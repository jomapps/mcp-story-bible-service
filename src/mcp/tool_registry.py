"""Tool registry for MCP WebSocket handling."""

from collections.abc import Awaitable, Callable
from typing import Any, Dict


ToolHandler = Callable[[Dict[str, Any]], Awaitable[Dict[str, Any]]]


class ToolRegistry:
    def __init__(self) -> None:
        self._registry: Dict[str, ToolHandler] = {}

    def register(self, name: str, handler: ToolHandler) -> None:
        self._registry[name] = handler

    def get(self, name: str) -> ToolHandler:
        if name not in self._registry:
            raise KeyError(f"Tool {name} is not registered")
        return self._registry[name]

    def list_tools(self) -> Dict[str, str]:
        return {name: handler.__doc__ or "" for name, handler in self._registry.items()}
