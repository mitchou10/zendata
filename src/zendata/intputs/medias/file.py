from pydantic import Field, HttpUrl
from pathlib import Path
from typing import Union, Optional
from ..base import BaseInput


class File(BaseInput):
    id: str = Field(..., description="Unique file ID")
    source: str = Field(
        ..., description="Source of the file (URL, file system, upload, etc.)"
    )
    filename: str = Field(..., description="Filename with extension")
    size: int = Field(..., ge=0, description="File size in bytes")
    save_path: Optional[Union[Path, HttpUrl]] = Field(
        None, description="Path to save file or URL if fetched from web"
    )
    checksum: Optional[str] = Field(None, description="File checksum (MD5/SHA256)")
