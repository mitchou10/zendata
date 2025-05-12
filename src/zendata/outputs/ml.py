import time
from pydantic import BaseModel, Field
from typing import Optional


class BaseOutput(BaseModel):
    id: str = Field(..., description="Unique identifier for the output")
    source_id: str = Field(
        ..., description="ID of the source from which this output is generated"
    )
    created_at: int = Field(
        default_factory=lambda _: int(time.time()),
        ge=0,
        description="Creation timestamp in seconds (Unix timestamp)",
    )
    model_name: Optional[str] = Field(
        None, description="Name of the model that generated this output"
    )
    model_version: Optional[str] = Field(
        None, description="Version of the model that generated this output"
    )
