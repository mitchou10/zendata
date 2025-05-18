from pydantic import Field, BaseModel
from zendata.data.ml.base import BaseMLData


class GroundTruthBbox(BaseModel):
    x: float = Field(..., ge=0.0, le=1.0, description="Relative x position (0<=x <=1)")
    y: float = Field(..., ge=0.0, le=1.0, description="Relative y position (0<=y <=1)")
    height: float = Field(
        ..., ge=0.0, le=1.0, description="Relative height position (0<=height <=1)"
    )
    width: float = Field(
        ..., ge=0.0, le=1.0, description="Relative width position (0<=width <=1)"
    )
    label: str = Field(..., description="Label of the bbox")


class PredictBbox(GroundTruthBbox):
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence of the class bbox (0<=Confidence <=1)",
    )


class GtImageDetection(BaseMLData):
    bboxes: list[GroundTruthBbox] = Field(
        default_factory=list, description="Ground truth bboxes"
    )


class PredictedImageDetection(BaseMLData):
    bboxes: list[PredictBbox] = Field(
        default_factory=list, description="Predicted bboxes"
    )
