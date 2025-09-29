"""Project level authorization helpers."""

from fastapi import Depends

from ..middleware.auth import get_current_user
from ..models import AuthenticatedUser
from ..utils.validation import ensure_project_access


async def require_project_access(
    project_id: str,
    user: AuthenticatedUser = Depends(get_current_user),
) -> AuthenticatedUser:
    ensure_project_access(project_id, user)
    return user
