from typing import Optional, Any, Dict
from enum import Enum
from datetime import datetime
from uuid import uuid4
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
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
    input: Optional[BaseModel] = Field(None, description="Input data")
    output: Optional[BaseModel] = Field(None, description="Output data")
    parameters: Optional[BaseModel] = Field(None, description="Parameters")
    error: Optional[str] = Field(None, description="Error message if task failed")
    extras: Dict[str, Any] = Field(
        default_factory=dict, description="Additional fields not defined in the model"
    )

    model_config = ConfigDict(extra="allow")

    
    @model_validator(mode="before")
    @classmethod
    def set_updated_at(cls, values):
        values["updated_at"] = int(datetime.now().timestamp())
        return values

    def update_updated_at(self):
        self.updated_at = int(datetime.now().timestamp())

    def set_status(self, status: TaskStatus, error: str = None):
        self.status = status
        self.update_updated_at()
        if error:
            self.error = error

    def set_status_to_created(self):
        self.set_status(TaskStatus.CREATED.value)

    def set_status_to_started(self):
        self.set_status(TaskStatus.STARTED.value)

    def set_status_to_in_progress(self):
        self.set_status(TaskStatus.IN_PROGRESS.value)

    def set_status_to_completed(self):
        self.percentage = 1
        self.set_status(TaskStatus.COMPLETED.value)

    def set_status_to_failed(self, error: str):
        self.set_status(TaskStatus.FAILED.value, error=error)

    def set_status_to_retrying(self, error: str = None):
        self.set_status(TaskStatus.RETRYING.value, error=error)

    def set_status_to_canceled(self, error: str):
        self.set_status(TaskStatus.CANCELED.value, error=error)

    def set_status_to_timeout(self, error: str):
        self.set_status(TaskStatus.TIMEOUT.value, error=error)
