"""Authentication data models."""

from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict


class AuthenticatedUser(BaseModel):
    """User information returned after validating a bearer token."""

    id: str = Field(..., description="PayloadCMS user identifier")
    email: Optional[str] = Field(None, description="User email")
    roles: List[str] = Field(default_factory=list, description="Role slugs assigned to the user")
    projects: List[str] = Field(
        default_factory=list,
        description="Project identifiers the user can access",
    )

    model_config = ConfigDict(extra="allow")
