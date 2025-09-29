"""Business logic for story bible operations."""

from typing import Any, Dict, List, Optional

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
from ..utils.exceptions import AuthorizationError, PayloadCMSException
from ..utils.validation import ensure_project_access
from .brain_client import BrainServiceClient
from .export_service import ExportService
from .payload_service import PayloadCMSService


class StoryBibleService:
    def __init__(
        self,
        payload_service: PayloadCMSService,
        brain_client: BrainServiceClient,
        export_service: ExportService,
    ) -> None:
        self._payload = payload_service
        self._brain = brain_client
        self._export = export_service

    async def list_story_bibles(self, project_id: str, user: AuthenticatedUser) -> Dict[str, Any]:
        ensure_project_access(project_id, user)
        return await self._payload.list_story_bibles(project_id)

    async def create_story_bible(
        self,
        data: StoryBibleCreate,
        user: AuthenticatedUser,
    ) -> Dict[str, Any]:
        ensure_project_access(data.project_id, user)
        payload = data.model_dump(exclude_none=True)
        payload["status"] = "draft"
        payload["created_by"] = user.id
        return await self._payload.create_story_bible(payload)

    async def get_story_bible(
        self,
        story_bible_id: str,
        user: AuthenticatedUser,
        *,
        populate: bool = True,
    ) -> Dict[str, Any]:
        story_bible = await self._payload.get_story_bible(story_bible_id, populate=populate)
        project_id = story_bible.get("project_id")
        if not project_id:
            raise PayloadCMSException("Story bible missing project_id")
        ensure_project_access(project_id, user)
        return story_bible

    async def update_story_bible(
        self,
        story_bible_id: str,
        data: StoryBibleUpdate,
        user: AuthenticatedUser,
    ) -> Dict[str, Any]:
        story_bible = await self.get_story_bible(story_bible_id, user, populate=False)
        payload = data.model_dump(exclude_none=True)
        if not payload:
            return story_bible
        updated = await self._payload.update_story_bible(story_bible_id, payload)
        await self._payload.log_change(
            {
                "story_bible": story_bible_id,
                "user": user.id,
                "changes": payload,
            }
        )
        return updated

    async def delete_story_bible(self, story_bible_id: str, user: AuthenticatedUser) -> Dict[str, Any]:
        await self.get_story_bible(story_bible_id, user, populate=False)
        return await self._payload.delete_story_bible(story_bible_id)

    async def add_character(
        self,
        data: CharacterCreate,
        user: AuthenticatedUser,
    ) -> Dict[str, Any]:
        story_bible_id = data.story_bible_id
        story_bible = await self.get_story_bible(story_bible_id, user, populate=False)
        payload = data.model_dump(by_alias=True, exclude_none=True)
        payload["story_bible"] = story_bible["id"]
        character = await self._payload.create_character(payload)
        for relationship in data.relationships:
            rel_payload = relationship.model_dump(exclude_none=True)
            rel_payload["story_bible"] = story_bible_id
            rel_payload.setdefault("character_from", character.get("id"))
            await self._payload.create_relationship(rel_payload)
        return character

    async def update_character(
        self,
        story_bible_id: str,
        character_id: str,
        payload: Dict[str, Any],
        user: AuthenticatedUser,
    ) -> Dict[str, Any]:
        await self.get_story_bible(story_bible_id, user, populate=False)
        return await self._payload.update_character(character_id, payload)

    async def add_scene(
        self,
        data: SceneCreate,
        user: AuthenticatedUser,
    ) -> Dict[str, Any]:
        story_bible = await self.get_story_bible(data.story_bible_id, user, populate=False)
        payload = data.model_dump(by_alias=True, exclude_none=True)
        payload["story_bible"] = story_bible["id"]
        return await self._payload.create_scene(payload)

    async def update_scene(
        self,
        story_bible_id: str,
        scene_id: str,
        data: SceneUpdate,
        user: AuthenticatedUser,
    ) -> Dict[str, Any]:
        await self.get_story_bible(story_bible_id, user, populate=False)
        payload = data.model_dump(exclude_none=True)
        return await self._payload.update_scene(scene_id, payload)

    async def create_plot_thread(
        self,
        data: PlotThreadCreate,
        user: AuthenticatedUser,
    ) -> Dict[str, Any]:
        await self.get_story_bible(data.story_bible_id, user, populate=False)
        payload = data.model_dump(by_alias=True, exclude_none=True)
        return await self._payload.create_plot_thread(payload)

    async def update_plot_thread(
        self,
        story_bible_id: str,
        thread_id: str,
        data: PlotThreadUpdate,
        user: AuthenticatedUser,
    ) -> Dict[str, Any]:
        await self.get_story_bible(story_bible_id, user, populate=False)
        payload = data.model_dump(exclude_none=True)
        return await self._payload.update_plot_thread(thread_id, payload)

    async def create_story_outline(
        self,
        data: StoryOutlineCreate,
        user: AuthenticatedUser,
    ) -> Dict[str, Any]:
        await self.get_story_bible(data.story_bible_id, user, populate=False)
        payload = data.model_dump(by_alias=True, exclude_none=True)
        return await self._payload.create_story_outline(payload)

    async def validate_story_consistency(
        self,
        story_bible_id: str,
        user: AuthenticatedUser,
    ) -> Dict[str, Any]:
        story_bible = await self.get_story_bible(story_bible_id, user, populate=True)
        return await self._brain.call_tool(
            "validate_story_consistency",
            {"story_bible": story_bible},
        )

    async def generate_character_arc(
        self,
        story_bible_id: str,
        character_id: str,
        user: AuthenticatedUser,
        context: Optional[str] = None,
    ) -> Dict[str, Any]:
        story_bible = await self.get_story_bible(story_bible_id, user, populate=True)
        character = next(
            (
                char
                for char in story_bible.get("characters", [])
                if char.get("id") == character_id
            ),
            None,
        )
        if not character:
            raise AuthorizationError(f"Character {character_id} not found in story bible {story_bible_id}")
        return await self._brain.call_tool(
            "generate_character_arc",
            {"character": character, "story_context": context or story_bible},
        )

    async def suggest_scene_transitions(
        self,
        story_bible_id: str,
        scene_id: str,
        user: AuthenticatedUser,
    ) -> Dict[str, Any]:
        story_bible = await self.get_story_bible(story_bible_id, user, populate=True)
        scene = next(
            (
                sc
                for sc in story_bible.get("scenes", [])
                if sc.get("id") == scene_id
            ),
            None,
        )
        if not scene:
            raise AuthorizationError(f"Scene {scene_id} not found in story bible {story_bible_id}")
        return await self._brain.call_tool(
            "suggest_scene_transitions",
            {"scene": scene, "story_bible": story_bible},
        )

    async def generate_export(
        self,
        story_bible_id: str,
        user: AuthenticatedUser,
        *,
        export_format: str,
        sections: Optional[List[str]] = None,
    ) -> bytes:
        story_bible = await self.get_story_bible(story_bible_id, user, populate=True)
        return self._export.generate(
            story_bible,
            export_format=export_format,
            sections=sections,
        )

    async def track_change(
        self,
        story_bible_id: str,
        user: AuthenticatedUser,
        changes: Dict[str, Any],
    ) -> Dict[str, Any]:
        await self.get_story_bible(story_bible_id, user, populate=False)
        payload = {"story_bible": story_bible_id, "user": user.id, "changes": changes}
        return await self._payload.log_change(payload)
