from io import BytesIO

import requests
from typing import NewType, Any
from cnninfer.dto.coco import COCODataset
from pycocotools.coco import COCO
from cnninfer.dto import coco


def init_coco_api(annotation_path: str) -> COCO:
    return COCO(annotation_file=annotation_path)


def get_coco_imageid(coco_api: COCO, num_image: int) -> list[coco.COCOImageID]:
    img_ids = coco_api.getImgIds()
    img_ids = [coco.COCOImageID(ids) for ids in coco_api.getImgIds()]
    return img_ids[:num_image]


def get_coco_annotations(
    coco_api: COCO, img_ids: list[coco.COCOImageID]
) -> list[coco.COCOAnnotations]:
    return coco_api.loadAnns(coco_api.getAnnIds(imgIds=img_ids))


def get_image_metadata(coco_api: COCO, img_ids: list[coco.COCOImageID]) -> Any | None:
    return [coco_api.loadImgs(img_id)[0] for img_id in img_ids]


def download_coco_images(coco_url: coco.COCOImageURL) -> coco.COCOImage:
    img_response = requests.get(coco_url, timeout=10)
    return coco.COCOImage(img_response.content)


# Provide Global Scope
coco_api: COCO = init_coco_api("./projects/inferengine/instances_val2017.json")
