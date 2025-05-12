import time
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class TypeInput(str, Enum):
    IMAGE = "image"
    FRAMES = "frames"
    TEXT = "text"
    AUDIO = "audio"
    VIDEO = "video"


class BaseInput(BaseModel):
    id: str = Field(..., description="Unique data ID")
    type: str = Field(..., description="Input Type")
    created_at: int = Field(
        default_factory=lambda _: int(time.time()),
        ge=0,
        description="Creation timestamp in seconds (Unix timestamp)",
    )
    version: Optional[str] = Field(None, description="Data version")
