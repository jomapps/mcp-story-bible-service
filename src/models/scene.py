"""Scene models for story bible management."""

from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, ConfigDict


class SceneCreate(BaseModel):
    story_bible_id: str = Field(..., alias="story_bible")
    sequence_number: int = Field(..., ge=1)
    title: str = Field(..., min_length=1, max_length=200)
    location: str = Field(..., min_length=1)
    time_of_day: Literal["dawn", "morning", "afternoon", "evening", "night"]
    scene_purpose: Literal[
        "setup",
        "conflict",
        "resolution",
        "character_development",
        "plot_advancement",
    ]
    description: str = Field(..., min_length=10)
    dialogue_notes: Optional[str] = None
    emotional_beats: List[str] = Field(default_factory=list)
    estimated_duration: Optional[int] = Field(None, ge=1)
    characters_present: List[str] = Field(default_factory=list)
    plot_threads: List[str] = Field(default_factory=list)

    model_config = ConfigDict(populate_by_name=True)


class SceneUpdate(BaseModel):
    sequence_number: Optional[int] = Field(None, ge=1)
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    location: Optional[str] = Field(None, min_length=1)
    time_of_day: Optional[
        Literal["dawn", "morning", "afternoon", "evening", "night"]
    ] = None
    scene_purpose: Optional[
        Literal[
            "setup",
            "conflict",
            "resolution",
            "character_development",
            "plot_advancement",
        ]
    ] = None
    description: Optional[str] = Field(None, min_length=10)
    dialogue_notes: Optional[str] = None
    emotional_beats: Optional[List[str]] = None
    estimated_duration: Optional[int] = Field(None, ge=1)
    characters_present: Optional[List[str]] = None
    plot_threads: Optional[List[str]] = None


class Scene(BaseModel):
    id: str
    story_bible: str
    sequence_number: int
    title: str
    location: str
    time_of_day: str
    scene_purpose: str
    description: str
    dialogue_notes: Optional[str]
    emotional_beats: List[str]
    estimated_duration: Optional[int]
    created_at: datetime
    updated_at: datetime
    characters_present: List[str] = Field(default_factory=list)
    plot_threads: List[str] = Field(default_factory=list)

    model_config = ConfigDict(extra="allow")
