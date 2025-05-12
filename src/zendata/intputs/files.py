import time
from pydantic import BaseModel, Field, HttpUrl
from pathlib import Path
from typing import Union, Optional, Literal


class File(BaseModel):
    id: str = Field(..., description="Unique file ID")
    type: Literal["csv", "json", "parquet", "excel"] = Field(
        ..., description="File type"
    )
    created_at: int = Field(
        default_factory=lambda _: int(time.time()),
        ge=0,
        description="Creation timestamp in seconds (Unix timestamp)",
    )
    source: str = Field(
        ..., description="Source of the file (URL, file system, upload, etc.)"
    )
    filename: str = Field(..., description="Filename with extension")
    size: int = Field(..., ge=0, description="File size in bytes")
    save_path: Optional[Union[Path, HttpUrl]] = Field(
        None, description="Path to save file or URL if fetched from web"
    )
    version: Optional[str] = Field(None, description="File version")
    checksum: Optional[str] = Field(None, description="File checksum (MD5/SHA256)")
