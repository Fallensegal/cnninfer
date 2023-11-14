from typing import Optional

from pycocotools.coco import COCO


def init_coco_api(annotation_path: str) -> COCO:
    return COCO(annotation_file=annotation_path)


def get_coco_image_ids(
    coco_api: COCO, num_image: int, cat_names: Optional[list[str]]
) -> list[int]:
    if cat_names:
        cat_ids = coco_api.getCatIds(catNms=cat_names)
        img_ids = coco_api.getImgIds(catIds=cat_ids)
    else:
        img_ids = coco_api.getImgIds()
    return img_ids[:num_image]
