from typing import Literal
from ..base import BaseData
from pydantic import Field


class TextInput(BaseData):
    type: Literal["text"] = "text"
    text: str = Field(..., description="Raw text")
