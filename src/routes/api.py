"""REST API routes for story bible management."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response, status

from ..middleware.auth import get_current_user
from ..models import (
    AuthenticatedUser,
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


router = APIRouter()


def get_story_service(request: Request) -> StoryBibleService:
    service: Optional[StoryBibleService] = getattr(request.app.state, "story_service", None)
    if service is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Story service not ready")
    return service


@router.get("/story-bibles")
async def list_story_bibles(
    project_id: str,
    service: StoryBibleService = Depends(get_story_service),
    user: AuthenticatedUser = Depends(get_current_user),
):
    return await service.list_story_bibles(project_id, user)


@router.post("/story-bibles", status_code=status.HTTP_201_CREATED)
async def create_story_bible(
    payload: StoryBibleCreate,
    service: StoryBibleService = Depends(get_story_service),
    user: AuthenticatedUser = Depends(get_current_user),
):
    return await service.create_story_bible(payload, user)


@router.get("/story-bibles/{story_bible_id}")
async def get_story_bible(
    story_bible_id: str,
    populate: bool = True,
    service: StoryBibleService = Depends(get_story_service),
    user: AuthenticatedUser = Depends(get_current_user),
):
    return await service.get_story_bible(story_bible_id, user, populate=populate)


@router.patch("/story-bibles/{story_bible_id}")
async def update_story_bible(
    story_bible_id: str,
    payload: StoryBibleUpdate,
    service: StoryBibleService = Depends(get_story_service),
    user: AuthenticatedUser = Depends(get_current_user),
):
    return await service.update_story_bible(story_bible_id, payload, user)


@router.delete("/story-bibles/{story_bible_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_story_bible(
    story_bible_id: str,
    service: StoryBibleService = Depends(get_story_service),
    user: AuthenticatedUser = Depends(get_current_user),
):
    await service.delete_story_bible(story_bible_id, user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/story-bibles/{story_bible_id}/characters", status_code=status.HTTP_201_CREATED)
async def add_character(
    story_bible_id: str,
    payload: CharacterCreate,
    service: StoryBibleService = Depends(get_story_service),
    user: AuthenticatedUser = Depends(get_current_user),
):
    updated = payload.model_copy(update={"story_bible_id": story_bible_id})
    return await service.add_character(updated, user)


@router.patch("/story-bibles/{story_bible_id}/characters/{character_id}")
async def update_character(
    story_bible_id: str,
    character_id: str,
    payload: dict,
    service: StoryBibleService = Depends(get_story_service),
    user: AuthenticatedUser = Depends(get_current_user),
):
    return await service.update_character(story_bible_id, character_id, payload, user)


@router.post("/story-bibles/{story_bible_id}/scenes", status_code=status.HTTP_201_CREATED)
async def add_scene(
    story_bible_id: str,
    payload: SceneCreate,
    service: StoryBibleService = Depends(get_story_service),
    user: AuthenticatedUser = Depends(get_current_user),
):
    updated = payload.model_copy(update={"story_bible_id": story_bible_id})
    return await service.add_scene(updated, user)


@router.patch("/story-bibles/{story_bible_id}/scenes/{scene_id}")
async def update_scene(
    story_bible_id: str,
    scene_id: str,
    payload: SceneUpdate,
    service: StoryBibleService = Depends(get_story_service),
    user: AuthenticatedUser = Depends(get_current_user),
):
    return await service.update_scene(story_bible_id, scene_id, payload, user)


@router.post("/story-bibles/{story_bible_id}/plot-threads", status_code=status.HTTP_201_CREATED)
async def create_plot_thread(
    story_bible_id: str,
    payload: PlotThreadCreate,
    service: StoryBibleService = Depends(get_story_service),
    user: AuthenticatedUser = Depends(get_current_user),
):
    updated = payload.model_copy(update={"story_bible_id": story_bible_id})
    return await service.create_plot_thread(updated, user)


@router.patch("/story-bibles/{story_bible_id}/plot-threads/{thread_id}")
async def update_plot_thread(
    story_bible_id: str,
    thread_id: str,
    payload: PlotThreadUpdate,
    service: StoryBibleService = Depends(get_story_service),
    user: AuthenticatedUser = Depends(get_current_user),
):
    return await service.update_plot_thread(story_bible_id, thread_id, payload, user)


@router.post("/story-bibles/{story_bible_id}/outline", status_code=status.HTTP_201_CREATED)
async def create_outline(
    story_bible_id: str,
    payload: StoryOutlineCreate,
    service: StoryBibleService = Depends(get_story_service),
    user: AuthenticatedUser = Depends(get_current_user),
):
    updated = payload.model_copy(update={"story_bible_id": story_bible_id})
    return await service.create_story_outline(updated, user)


@router.post("/story-bibles/{story_bible_id}/consistency")
async def validate_consistency(
    story_bible_id: str,
    service: StoryBibleService = Depends(get_story_service),
    user: AuthenticatedUser = Depends(get_current_user),
):
    return await service.validate_story_consistency(story_bible_id, user)


@router.post("/story-bibles/{story_bible_id}/characters/{character_id}/arc")
async def generate_character_arc(
    story_bible_id: str,
    character_id: str,
    story_context: Optional[str] = None,
    service: StoryBibleService = Depends(get_story_service),
    user: AuthenticatedUser = Depends(get_current_user),
):
    return await service.generate_character_arc(
        story_bible_id,
        character_id,
        user,
        context=story_context,
    )


@router.post("/story-bibles/{story_bible_id}/scenes/{scene_id}/transitions")
async def suggest_scene_transitions(
    story_bible_id: str,
    scene_id: str,
    service: StoryBibleService = Depends(get_story_service),
    user: AuthenticatedUser = Depends(get_current_user),
):
    return await service.suggest_scene_transitions(story_bible_id, scene_id, user)


@router.get("/story-bibles/{story_bible_id}/export")
async def export_story_bible(
    story_bible_id: str,
    format: str = "markdown",
    sections: Optional[List[str]] = Query(default=None),
    service: StoryBibleService = Depends(get_story_service),
    user: AuthenticatedUser = Depends(get_current_user),
):
    content = await service.generate_export(
        story_bible_id,
        user,
        export_format=format,
        sections=sections,
    )
    media_type = {
        "markdown": "text/markdown",
        "json": "application/json",
        "pdf": "application/pdf",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }.get(format.lower(), "application/octet-stream")
    filename = f"story-bible-{story_bible_id}.{format.lower()}"
    headers = {"Content-Disposition": f"attachment; filename={filename}"}
    return Response(content=content, media_type=media_type, headers=headers)


@router.post("/story-bibles/{story_bible_id}/changes")
async def track_story_bible_change(
    story_bible_id: str,
    changes: dict,
    service: StoryBibleService = Depends(get_story_service),
    user: AuthenticatedUser = Depends(get_current_user),
):
    return await service.track_change(story_bible_id, user, changes)
