"""Story outline models."""

from typing import List, Literal, Optional

from pydantic import BaseModel, Field, ConfigDict


class StoryOutlineCreate(BaseModel):
    story_bible_id: str = Field(..., alias="story_bible")
    act_structure: Literal["three_act", "five_act", "hero_journey"]
    genre_conventions: List[str] = Field(default_factory=list)
    plot_points: List[str] = Field(default_factory=list)
    estimated_runtime: Optional[int] = Field(None, ge=1)
    target_audience: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)


class StoryOutline(BaseModel):
    id: str
    story_bible: str
    act_structure: str
    genre_conventions: List[str]
    plot_points: List[str]
    estimated_runtime: Optional[int]
    target_audience: Optional[str]

    model_config = ConfigDict(extra="allow")
