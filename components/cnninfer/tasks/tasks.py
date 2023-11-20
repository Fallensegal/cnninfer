import json

import dramatiq
from pathlib import Path
from mmdet.apis import DetInferencer
from cnninfer.storage import s3storage
from cnninfer.mmdetinfer import mmdetect

from components.cnninfer.coco.api import (
    coco_api,
    download_coco_images,
    get_coco_imageid,
    get_image_metadata,
    get_coco_annotations,
)

from components.cnninfer.dto.coco import (
    COCOInferResults,
    COCODataset,
    COCOModelMeta,
    COCOImageID,
    COCOImageURL,
    COCOImageName,
)

from typing import Any

infer_dataset: list[COCODataset] = []
BUCKETS: list[str] = [
    "preimages",
    "postimages-frcnn",
    "postimages-srcnn",
    "postimages-detr",
    "eval-graphs",
]


@dramatiq.actor(store_results=True)
def prepare_coco_dataset(num_pictures: int) -> str:
    [
        s3storage.create_bucket(s3storage.minio_client, bucket_name)
        for bucket_name in BUCKETS
    ]

    # Upload COCO Dataset to Bucket
    img_ids = get_coco_imageid(coco_api=coco_api, num_image=num_pictures)
    imgs_metadata = get_image_metadata(coco_api=coco_api, img_ids=img_ids)
    img_names = [COCOImageName(f"img_{id}") for id in img_ids]
    img_urls = [COCOImageURL(img["coco_url"]) for img in imgs_metadata]
    img_annotations = [get_coco_annotations(coco_api, img_id) for img_id in img_ids]
    img_content = [download_coco_images(url) for url in img_urls]

    [
        s3storage.upload_file_from_bytes(
            minio_client=s3storage.minio_client,
            bucket_name="preimages",
            object_name=f"{name}.jpg",
            file_content=content,
            content_length=len(content),
        )
        for name, content in zip(img_names, img_content, strict=True)
    ]
    global infer_dataset
    infer_dataset = [
        COCODataset(img_id=id, img_url=url, img_name=name, img_annotations=annotation)
        for id, url, name, annotation in zip(
            img_ids, img_urls, img_names, img_annotations, strict=True
        )
    ]

    return "Bucket Image Init Successful"


@dramatiq.actor(store_results=True)
def infer_and_calculate_results_pipeline() -> str:

    urls = [f.img_url for f in infer_dataset]
    msg = infer_images.send(urls, mmdetect.detr_meta.model_dump())
    _ = msg.get_result(timeout=100_000, block=True)

    return "Something Happend"


@dramatiq.actor(store_results=True)
def infer_images(
    coco_urls: list[COCOImageURL], model_meta: dict[str, Any]
) -> list[dict[str, Any]]:

    model_meta_pyd = COCOModelMeta(**model_meta)
    if model_meta_pyd.name == "srcnn":
        model = DetInferencer("sparse-rcnn_r50_fpn_1x_coco", device="cpu")
    elif model_meta_pyd.name == "frcnn":
        model = DetInferencer("faster-rcnn_r50_fpn_1x_coco", device="cpu")
    else:
        model = DetInferencer("ddq-detr-4scale_r50_8xb2-12e_coco", device="cpu")

    id_fname: list[tuple[str, COCOImageID]] = []
    
    result = [model(url, out_dir=model_meta_pyd.savefile_dir) for url in coco_urls]
    f_paths = [f"./{path!s}" for path in Path(f"{model_meta_pyd.savefile_dir}/vis/").glob("*")]
    f_list = [f.name for f in Path(f"{model_meta_pyd.savefile_dir}/vis/").glob("*")]
    img_ids = get_coco_imageid(coco_api=coco_api, num_image=len(f_list))

    for fname, id in zip(f_list, img_ids, strict=True):
        id_fname.append((fname, id))

    [
        s3storage.upload_file_from_fs(
            minio_client=s3storage.minio_client,
            bucket_name=model_meta_pyd.s3_bucket,
            obj_name=obj_name,
            file_path=f_path,
        )
        for obj_name, f_path in zip(f_list, f_paths, strict=True)
    ]

    modeled_result = [
        COCOInferResults(results=rslt, id_to_fname=meta, s3_bucket=model_meta_pyd.s3_bucket)
        for rslt, meta in zip(result, id_fname, strict=True)
    ]

    return  [item.model_dump() for item in modeled_result]

"""
@dramatiq.actor
def startEverything() -> None:
    download Files
    upload to s3 bucket
    submit each file for inference
    submit experiment data result per file
    """
