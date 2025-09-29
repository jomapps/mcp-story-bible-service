"""Story bible domain models."""

from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, ConfigDict


class StoryBibleCreate(BaseModel):
    project_id: str = Field(..., description="Parent project identifier")
    title: str = Field(..., min_length=1, max_length=200)
    genre: str = Field(..., min_length=1, max_length=100)
    premise: str = Field(..., min_length=10)
    logline: Optional[str] = Field(None, max_length=300)
    themes: List[str] = Field(default_factory=list)


class StoryBibleUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    genre: Optional[str] = Field(None, min_length=1, max_length=100)
    premise: Optional[str] = Field(None, min_length=10)
    logline: Optional[str] = Field(None, max_length=300)
    treatment: Optional[str] = None
    themes: Optional[List[str]] = None
    status: Optional[Literal["draft", "in_progress", "completed"]] = None


class StoryBibleSummary(BaseModel):
    id: str
    project_id: str
    title: str
    genre: str
    status: Literal["draft", "in_progress", "completed"]
    updated_at: datetime


class StoryBible(BaseModel):
    id: str
    project_id: str
    title: str
    genre: str
    premise: str
    logline: Optional[str]
    treatment: Optional[str]
    themes: List[str]
    status: Literal["draft", "in_progress", "completed"]
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str]

    model_config = ConfigDict(extra="allow")
