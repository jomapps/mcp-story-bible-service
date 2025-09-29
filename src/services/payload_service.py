"""Async client for interacting with PayloadCMS (Auto-Movie) collections."""

from typing import Any, Dict, Optional

import httpx
from tenacity import AsyncRetrying, retry_if_exception_type, stop_after_attempt, wait_exponential

from ..utils.exceptions import PayloadCMSException


class PayloadCMSService:
    def __init__(
        self,
        base_url: str,
        api_key: Optional[str],
        timeout: float,
        max_retries: int,
    ) -> None:
        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        self._client = httpx.AsyncClient(
            base_url=base_url,
            timeout=httpx.Timeout(timeout),
            headers=headers,
        )
        self._max_retries = max_retries

    async def aclose(self) -> None:
        await self._client.aclose()

    async def _request(
        self,
        method: str,
        url: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        async for attempt in AsyncRetrying(
            stop=stop_after_attempt(self._max_retries),
            wait=wait_exponential(multiplier=1, min=1, max=5),
            retry=retry_if_exception_type(httpx.HTTPError),
            reraise=True,
        ):
            with attempt:
                response = await self._client.request(method, url, params=params, json=json)
                response.raise_for_status()
                data = response.json()
                if isinstance(data, dict) and "doc" in data:
                    return data["doc"]
                return data

        raise PayloadCMSException(f"Failed to call PayloadCMS {method} {url}")

    async def list_story_bibles(self, project_id: str) -> Dict[str, Any]:
        return await self._request(
            "GET",
            "/api/story-bibles",
            params={"where[project_id][equals]": project_id, "limit": 50},
        )

    async def create_story_bible(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self._request("POST", "/api/story-bibles", json=payload)

    async def get_story_bible(self, story_bible_id: str, populate: bool = True) -> Dict[str, Any]:
        params = {"depth": 2} if populate else None
        return await self._request("GET", f"/api/story-bibles/{story_bible_id}", params=params)

    async def update_story_bible(self, story_bible_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self._request("PATCH", f"/api/story-bibles/{story_bible_id}", json=payload)

    async def delete_story_bible(self, story_bible_id: str) -> Dict[str, Any]:
        return await self._request("DELETE", f"/api/story-bibles/{story_bible_id}")

    async def create_character(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self._request("POST", "/api/story-bible-characters", json=payload)

    async def update_character(self, character_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self._request(
            "PATCH",
            f"/api/story-bible-characters/{character_id}",
            json=payload,
        )

    async def delete_character(self, character_id: str) -> Dict[str, Any]:
        return await self._request("DELETE", f"/api/story-bible-characters/{character_id}")

    async def create_relationship(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self._request("POST", "/api/character-relationships", json=payload)

    async def create_scene(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self._request("POST", "/api/story-bible-scenes", json=payload)

    async def update_scene(self, scene_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self._request("PATCH", f"/api/story-bible-scenes/{scene_id}", json=payload)

    async def delete_scene(self, scene_id: str) -> Dict[str, Any]:
        return await self._request("DELETE", f"/api/story-bible-scenes/{scene_id}")

    async def create_plot_thread(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self._request("POST", "/api/plot-threads", json=payload)

    async def update_plot_thread(self, thread_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self._request("PATCH", f"/api/plot-threads/{thread_id}", json=payload)

    async def delete_plot_thread(self, thread_id: str) -> Dict[str, Any]:
        return await self._request("DELETE", f"/api/plot-threads/{thread_id}")

    async def create_story_outline(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self._request("POST", "/api/story-outlines", json=payload)

    async def log_change(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self._request("POST", "/api/story-bible-changes", json=payload)
