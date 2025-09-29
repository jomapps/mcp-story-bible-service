import pytest
from unittest.mock import AsyncMock, MagicMock

from src.models import (
    AuthenticatedUser,
    StoryBibleCreate,
)
from src.services.story_bible_service import StoryBibleService


@pytest.fixture
def user() -> AuthenticatedUser:
    return AuthenticatedUser(id="user-1", email="user@example.com", roles=["writer"], projects=["proj-1"])


@pytest.mark.asyncio
async def test_create_story_bible_success(user: AuthenticatedUser):
    payload_service = AsyncMock()
    payload_service.create_story_bible.return_value = {"id": "sb-1", "project_id": "proj-1"}
    payload_service.list_story_bibles.return_value = {}
    payload_service.get_story_bible.return_value = {"id": "sb-1", "project_id": "proj-1"}

    brain_client = AsyncMock()
    export_service = MagicMock()

    service = StoryBibleService(payload_service, brain_client, export_service)

    data = StoryBibleCreate(
        project_id="proj-1",
        title="Test",
        genre="Drama",
        premise="A compelling tale of courage",
    )
    result = await service.create_story_bible(data, user)

    payload_service.create_story_bible.assert_awaited()
    assert result["id"] == "sb-1"


@pytest.mark.asyncio
async def test_generate_export_uses_export_service(user: AuthenticatedUser):
    payload_service = AsyncMock()
    payload_service.get_story_bible.return_value = {
        "id": "sb-1",
        "project_id": "proj-1",
        "title": "Story",
        "genre": "Drama",
        "premise": "Premise",
    }

    brain_client = AsyncMock()
    export_service = MagicMock()
    export_service.generate.return_value = b"content"

    service = StoryBibleService(payload_service, brain_client, export_service)

    content = await service.generate_export("sb-1", user, export_format="markdown")

    payload_service.get_story_bible.assert_awaited_with("sb-1", populate=True)
    export_service.generate.assert_called_once()
    assert content == b"content"
