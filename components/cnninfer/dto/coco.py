from datetime import timedelta
from io import BytesIO
from typing import Any, NewType 
import requests
from mmdet.apis import DetInferencer
from pydantic import BaseModel

COCOImageName = NewType("COCOImageName", str)
COCOImageID = NewType("COCOImageID", int)
COCOImageURL = NewType("COCOImageURL", str)
COCOAnnotations = NewType("COCOAnnotations", dict)
COCOResults = NewType("COCOResults", dict)
COCOImage = NewType("COCOImage", bytes)
MeanAP = NewType("MeanAP", float)
class COCODataset(BaseModel):
    img_id: COCOImageID
    img_url: COCOImageURL
    img_name: COCOImageName
    img_annotations: list[COCOAnnotations]

class COCOModelMeta(BaseModel):
    name: str
    s3_bucket: str
    savefile_dir: str

class COCOInferResults(BaseModel):
    results: COCOResults
    id_to_fname: tuple[str, COCOImageID]
    s3_bucket: str
