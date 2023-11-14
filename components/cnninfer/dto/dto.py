from datetime import timedelta

from pydantic import BaseModel


class Annotations(BaseModel):
    label: str
    confidence: float


class ExperimentData(BaseModel):
    processing_time: timedelta
    picture_label: list[Annotations]


class ExperimentResult(BaseModel):
    before_picture: bytes
    after_picture: bytes
    experiment_data: ExperimentData


class ExperimentResponse(BaseModel):
    result: list[ExperimentResult]
