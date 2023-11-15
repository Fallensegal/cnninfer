from datetime import timedelta
from io import BytesIO
from typing import Any 
import requests
from pydantic import BaseModel


class COCODataset(BaseModel):
    img_id_list: list[int]
    img_name_list: list[str]
    image_list: list[bytes]
    image_annotations: Any | None

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
