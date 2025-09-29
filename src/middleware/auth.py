"""Bearer authentication middleware helpers."""

from typing import Optional

import httpx
from fastapi import Depends, Header, HTTPException, status

from ..config import settings
from ..models import AuthenticatedUser


_auth_client = httpx.AsyncClient(timeout=httpx.Timeout(10.0))


async def verify_bearer_token(authorization: Optional[str] = Header(default=None)) -> AuthenticatedUser:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header with Bearer token required",
        )
    token = authorization.removeprefix("Bearer ").strip()
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = await _auth_client.get(f"{settings.PAYLOADCMS_API_URL}/api/users/me", headers=headers)
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token") from exc
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Failed to verify token with PayloadCMS") from exc

    payload = response.json()
    if isinstance(payload, dict) and "doc" in payload:
        payload = payload["doc"]
    return AuthenticatedUser.model_validate(payload)


async def get_current_user(user: AuthenticatedUser = Depends(verify_bearer_token)) -> AuthenticatedUser:
    return user
