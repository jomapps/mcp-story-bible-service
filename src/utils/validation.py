"""Validation helpers for service inputs."""

from fastapi import HTTPException, status

from ..models import AuthenticatedUser


def ensure_project_access(project_id: str, user: AuthenticatedUser) -> None:
    if project_id not in set(user.projects):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User {user.id} does not have access to project {project_id}",
        )
