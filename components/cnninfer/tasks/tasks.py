import json

import dramatiq
from cnninfer.storage import s3storage

from components.cnninfer.coco.api import (
    coco_api,
    download_coco_images,
    get_coco_imageid,
    get_image_metadata,
    get_coco_annotations,
)

from components.cnninfer.dto.coco import (
    COCOImage,
    COCOImageID,
    COCOImageURL,
    COCOImageName,
)
from components.cnninfer.dto.coco import COCODataset

infer_dataset: list[COCODataset] = []

@dramatiq.actor(store_results=True)
def get_first_url() -> str:
    return f"{infer_dataset[0].img_url}"


@dramatiq.actor(store_results=True)
def hello(name: str) -> str:
    saved_string = f"Hello {name}"
    print(saved_string)
    return saved_string


@dramatiq.actor(store_results=True)
def prepare_coco_dataset(num_pictures: int) -> str:
    buckets = [
        "preimages",
        "postimages-frcnn",
        "postimages-srcnn",
        "postimages-detr",
    ]

    [
        s3storage.create_bucket(s3storage.minio_client, bucket_name)
        for bucket_name in buckets
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
            object_name=name,
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


"""
@dramatiq.actor
def startEverything() -> None:
    download Files
    upload to s3 bucket
    submit each file for inference
    submit experiment data result per file
    """
