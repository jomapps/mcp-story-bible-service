"""MCP WebSocket endpoint."""

import base64
import logging
from typing import Any, Dict

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, status

from ..middleware.auth import verify_bearer_token
from ..models import (
    CharacterCreate,
    PlotThreadCreate,
    PlotThreadUpdate,
    SceneCreate,
    SceneUpdate,
    StoryBibleCreate,
    StoryBibleUpdate,
    StoryOutlineCreate,
)
from ..services.story_bible_service import StoryBibleService
from ..utils.exceptions import ServiceError
from ..utils.validation import ensure_project_access
from ..mcp.protocol import build_error_response, build_success_response
from ..mcp.tool_registry import ToolRegistry


logger = logging.getLogger(__name__)
router = APIRouter()


def _get_service(websocket: WebSocket) -> StoryBibleService:
    service = getattr(websocket.app.state, "story_service", None)
    if service is None:
        raise RuntimeError("Story bible service not initialised")
    return service


def _register_tools(service: StoryBibleService, user) -> ToolRegistry:
    registry = ToolRegistry()

    async def wrap_story_bible_create(arguments: Dict[str, Any]) -> Dict[str, Any]:
        payload = StoryBibleCreate.model_validate(arguments)
        return await service.create_story_bible(payload, user)

    async def wrap_story_bible_update(arguments: Dict[str, Any]) -> Dict[str, Any]:
        story_bible_id = arguments.get("story_bible_id")
        if not story_bible_id:
            raise ServiceError("story_bible_id is required")
        payload = StoryBibleUpdate.model_validate(arguments.get("data", {}))
        return await service.update_story_bible(story_bible_id, payload, user)

    async def wrap_get(arguments: Dict[str, Any]) -> Dict[str, Any]:
        story_bible_id = arguments.get("story_bible_id")
        if not story_bible_id:
            raise ServiceError("story_bible_id is required")
        populate = bool(arguments.get("populate", True))
        return await service.get_story_bible(story_bible_id, user, populate=populate)

    async def wrap_character(arguments: Dict[str, Any]) -> Dict[str, Any]:
        payload = CharacterCreate.model_validate(arguments)
        ensure_project_access(payload.story_bible_id, user)
        return await service.add_character(payload, user)

    async def wrap_scene(arguments: Dict[str, Any]) -> Dict[str, Any]:
        story_bible_id = arguments.get("story_bible_id")
        payload = SceneCreate.model_validate(arguments)
        payload.story_bible_id = story_bible_id or payload.story_bible_id
        return await service.add_scene(payload, user)

    async def wrap_scene_update(arguments: Dict[str, Any]) -> Dict[str, Any]:
        story_bible_id = arguments.get("story_bible_id")
        scene_id = arguments.get("scene_id")
        if not story_bible_id or not scene_id:
            raise ServiceError("story_bible_id and scene_id are required")
        payload = SceneUpdate.model_validate(arguments.get("data", {}))
        return await service.update_scene(story_bible_id, scene_id, payload, user)

    async def wrap_plot_thread(arguments: Dict[str, Any]) -> Dict[str, Any]:
        payload = PlotThreadCreate.model_validate(arguments)
        return await service.create_plot_thread(payload, user)

    async def wrap_plot_thread_update(arguments: Dict[str, Any]) -> Dict[str, Any]:
        story_bible_id = arguments.get("story_bible_id")
        thread_id = arguments.get("thread_id")
        if not story_bible_id or not thread_id:
            raise ServiceError("story_bible_id and thread_id are required")
        payload = PlotThreadUpdate.model_validate(arguments.get("data", {}))
        return await service.update_plot_thread(story_bible_id, thread_id, payload, user)

    async def wrap_outline(arguments: Dict[str, Any]) -> Dict[str, Any]:
        payload = StoryOutlineCreate.model_validate(arguments)
        return await service.create_story_outline(payload, user)

    async def wrap_consistency(arguments: Dict[str, Any]) -> Dict[str, Any]:
        story_bible_id = arguments.get("story_bible_id")
        if not story_bible_id:
            raise ServiceError("story_bible_id is required")
        return await service.validate_story_consistency(story_bible_id, user)

    async def wrap_character_arc(arguments: Dict[str, Any]) -> Dict[str, Any]:
        story_bible_id = arguments.get("story_bible_id")
        character_id = arguments.get("character_id")
        if not story_bible_id or not character_id:
            raise ServiceError("story_bible_id and character_id are required")
        return await service.generate_character_arc(
            story_bible_id,
            character_id,
            user,
            context=arguments.get("story_context"),
        )

    async def wrap_scene_transitions(arguments: Dict[str, Any]) -> Dict[str, Any]:
        story_bible_id = arguments.get("story_bible_id")
        scene_id = arguments.get("scene_id")
        if not story_bible_id or not scene_id:
            raise ServiceError("story_bible_id and scene_id are required")
        return await service.suggest_scene_transitions(story_bible_id, scene_id, user)

    async def wrap_export(arguments: Dict[str, Any]) -> Dict[str, Any]:
        story_bible_id = arguments.get("story_bible_id")
        export_format = arguments.get("format", "markdown")
        sections = arguments.get("sections")
        data = await service.generate_export(
            story_bible_id,
            user,
            export_format=export_format,
            sections=sections,
        )
        return {
            "story_bible_id": story_bible_id,
            "format": export_format,
            "content_b64": base64.b64encode(data).decode("utf-8"),
        }

    registry.register("create_story_bible", wrap_story_bible_create)
    registry.register("update_story_bible", wrap_story_bible_update)
    registry.register("get_story_bible", wrap_get)
    registry.register("add_character", wrap_character)
    registry.register("add_scene", wrap_scene)
    registry.register("update_scene", wrap_scene_update)
    registry.register("create_plot_thread", wrap_plot_thread)
    registry.register("update_plot_thread", wrap_plot_thread_update)
    registry.register("create_story_outline", wrap_outline)
    registry.register("validate_story_consistency", wrap_consistency)
    registry.register("generate_character_arc", wrap_character_arc)
    registry.register("suggest_scene_transitions", wrap_scene_transitions)
    registry.register("generate_story_bible_export", wrap_export)

    return registry


@router.websocket("/ws")
async def mcp_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        auth_header = websocket.headers.get("Authorization")
        user = await verify_bearer_token(authorization=auth_header)
    except HTTPException as exc:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise exc

    service = _get_service(websocket)
    registry = _register_tools(service, user)

    try:
        while True:
            message = await websocket.receive_json()
            method = message.get("method")
            request_id = message.get("id")
            params = message.get("params", {})

            if method == "list_tools":
                await websocket.send_json(
                    build_success_response(request_id, {"tools": registry.list_tools()})
                )
                continue

            if method != "call_tool":
                await websocket.send_json(
                    build_error_response(request_id, f"Unsupported method {method}"),
                )
                continue

            tool_name = params.get("name")
            arguments: Dict[str, Any] = params.get("arguments", {})
            try:
                handler = registry.get(tool_name)
                result = await handler(arguments)
                await websocket.send_json(build_success_response(request_id, result))
            except KeyError:
                await websocket.send_json(build_error_response(request_id, f"Unknown tool {tool_name}"))
            except ServiceError as exc:
                await websocket.send_json(build_error_response(request_id, str(exc)))
            except Exception as exc:  # noqa: BLE001
                logger.exception("Unhandled MCP tool error")
                await websocket.send_json(build_error_response(request_id, str(exc)))

    except WebSocketDisconnect:
        logger.debug("MCP client disconnected")
