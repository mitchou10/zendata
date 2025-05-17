from typing import Type, Optional, Any, Dict
from enum import Enum
from datetime import datetime
from uuid import uuid4
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
    field_serializer,
)


class TaskStatus(str, Enum):
    CREATED = "created"  # Task instantiated but not yet enqueued
    QUEUED = "queued"  # Waiting in a processing queue
    STARTED = "started"  # Has started processing
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"  # Successfully processed
    FAILED = "failed"  # Fatal error occurred
    RETRYING = "retrying"  # Being retried after a failure
    CANCELED = "canceled"  # Manually canceled or by business logic
    TIMEOUT = "timeout"  # Could not complete within the allowed time


class BaseTask(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex, description="Id of the task")
    name: str = Field(default_factory=lambda: uuid4().hex, description="Id of the task")
    status: TaskStatus = Field(TaskStatus.CREATED.value, description="Task status")
    percentage: float = Field(
        0.0, ge=0.0, le=1.0, description="Percentage of process (between 0 and 1)"
    )
    created_at: int = Field(
        default_factory=lambda: int(datetime.now().timestamp()),
        description="Created timestamp",
    )
    updated_at: Optional[int] = Field(None, description="Last updated timestamp")
    input: Optional[Type[Any]] = Field(None, description="Input Type")
    output: Optional[Type[Any]] = Field(None, description="Output Type")
    error: Optional[str] = Field(None, description="Error message if task failed")
    extras: Dict[str, Any] = Field(
        default_factory=dict, description="Additional fields not defined in the model"
    )

    model_config = ConfigDict(extra="allow")

    @field_serializer("input")
    def serialize_input(self, v: Type[Any], _info):
        return v.__name__ if v else None

    @field_serializer("output")
    def serialize_output(self, v: Type[Any], _info):
        return v.__name__ if v else None

    @field_validator("input", "output", mode="before")
    @classmethod
    def check_is_type(cls, v, field):
        if v is not None and not isinstance(v, type):
            raise TypeError(f"{field.field_name} must be a type, got {type(v)}")
        return v

    @model_validator(mode="before")
    @classmethod
    def set_updated_at(cls, values):
        values["updated_at"] = int(datetime.now().timestamp())
        return values
