"""API response wrappers."""

from typing import Any, Dict, Generic, Optional, TypeVar

from pydantic import BaseModel, Field


T = TypeVar("T")


class ServiceResponse(BaseModel, Generic[T]):
    success: bool = Field(...)
    data: Optional[T] = Field(default=None)
    error: Optional[str] = Field(default=None)
    meta: Dict[str, Any] = Field(default_factory=dict)
