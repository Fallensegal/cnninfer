
from io import BytesIO

import requests
from cnninfer.dto.coco import COCODataset
from pycocotools.coco import COCO


def init_coco_api(annotation_path: str) -> COCO:
    return COCO(annotation_file=annotation_path)


def get_coco_image_ids(
    coco_api: COCO, num_image: int, cat_names: list[str] | None
) -> list[int]:
    if cat_names:
        cat_ids = coco_api.getCatIds(catNms=cat_names)
        img_ids = coco_api.getImgIds(catIds=cat_ids)
    else:
        img_ids = coco_api.getImgIds()
    return img_ids[:num_image]


def download_coco_images(coco_api: COCO, img_ids: list[int]) -> COCODataset:
    images_byte_list: list[bytes] = []
    image_name_list: list[str] = []
    for img_id in img_ids:
        img = coco_api.loadImgs(img_id)[0]
        img_url = img["coco_url"]
        img_response = requests.get(img_url, timeout=10)
        image_name_list.append(f"img_{img_id}")
        images_byte_list.append(img_response.content)
    image_annotations = coco_api.loadAnns(coco_api.getAnnIds(imgIds=img_ids))

    return COCODataset(
        img_name_list=image_name_list,
        img_id_list=img_ids,
        image_list=images_byte_list,
        image_annotations=image_annotations
    )
