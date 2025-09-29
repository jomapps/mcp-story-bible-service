"""Character models for story bible management."""

from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, ConfigDict


class CharacterRelationshipCreate(BaseModel):
    character_from: str = Field(..., description="Source character ID")
    character_to: str = Field(..., description="Target character ID")
    relationship_type: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    strength: Optional[int] = Field(None, ge=1, le=10)


class CharacterRelationship(CharacterRelationshipCreate):
    id: str
    story_bible: Optional[str] = None

    model_config = ConfigDict(extra="allow")


class CharacterCreate(BaseModel):
    story_bible_id: str = Field(..., alias="story_bible")
    name: str = Field(..., min_length=1, max_length=120)
    role: Literal["protagonist", "antagonist", "supporting", "minor"]
    background: str = Field(..., min_length=5)
    motivation: str = Field(..., min_length=5)
    arc_description: str = Field(..., min_length=5)
    physical_description: Optional[str] = None
    personality_traits: List[str] = Field(default_factory=list)
    dialogue_style: Optional[str] = None
    relationships: List[CharacterRelationshipCreate] = Field(default_factory=list)

    model_config = ConfigDict(populate_by_name=True)


class Character(BaseModel):
    id: str
    story_bible: str
    name: str
    role: str
    background: str
    motivation: str
    arc_description: str
    physical_description: Optional[str]
    personality_traits: List[str]
    dialogue_style: Optional[str]
    created_at: datetime
    updated_at: datetime
    relationships: List[CharacterRelationship] = Field(default_factory=list)

    model_config = ConfigDict(extra="allow")
