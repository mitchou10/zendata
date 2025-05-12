from pydantic import BaseModel, Field
from .labels import Label, MultiLabels


class Sequence(BaseModel):
    start: int = Field(..., ge=0, description="Start index of the sequence")
    end: int = Field(..., ge=0, description="End index of the sequence")


class SequenceLabel(Sequence, Label): ...


class SequenceMultLabel(Sequence, MultiLabels): ...
