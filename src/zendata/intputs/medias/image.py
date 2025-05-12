from pydantic import Field
from .file import File


class Image(File):
    width: int = Field(..., description="Width of the image in pixels")
    height: int = Field(..., description="Height of the image in pixels")
    format: str = Field(..., description="Format of the image (e.g., png, jpeg, gif)")
