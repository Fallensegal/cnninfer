from datetime import timedelta
from io import BytesIO
from typing import Any, NewType 
import requests
from pydantic import BaseModel

COCOImageName = NewType("COCOImageName", str)
COCOImageID = NewType("COCOImageID", int)
COCOImageURL = NewType("COCOImageURL", str)
COCOResult = NewType("COCOResult", dict)
COCOAnnotations = NewType("COCOAnnotations", dict)
COCOImage = NewType("COCOImage", bytes)
MeanAP = NewType("MeanAP", float)
class COCODataset(BaseModel):
    img_id: COCOImageID
    img_url: COCOImageURL
    img_name: COCOImageName
    img_annotations: list[COCOAnnotations]

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
