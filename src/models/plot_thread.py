"""Plot thread models."""

from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, ConfigDict


class PlotThreadCreate(BaseModel):
    story_bible_id: str = Field(..., alias="story_bible")
    thread_name: str = Field(..., min_length=1, max_length=150)
    thread_type: Literal["main_plot", "subplot", "character_arc", "theme"]
    description: str = Field(..., min_length=5)
    introduction_scene: Optional[str] = None
    resolution_scene: Optional[str] = None
    status: Literal["active", "resolved", "abandoned"] = "active"
    key_scenes: List[str] = Field(default_factory=list)

    model_config = ConfigDict(populate_by_name=True)


class PlotThreadUpdate(BaseModel):
    thread_name: Optional[str] = Field(None, min_length=1, max_length=150)
    thread_type: Optional[Literal["main_plot", "subplot", "character_arc", "theme"]] = None
    description: Optional[str] = Field(None, min_length=5)
    introduction_scene: Optional[str] = None
    resolution_scene: Optional[str] = None
    status: Optional[Literal["active", "resolved", "abandoned"]] = None
    key_scenes: Optional[List[str]] = None


class PlotThread(BaseModel):
    id: str
    story_bible: str
    thread_name: str
    thread_type: str
    description: str
    introduction_scene: Optional[str]
    resolution_scene: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime
    key_scenes: List[str] = Field(default_factory=list)

    model_config = ConfigDict(extra="allow")
