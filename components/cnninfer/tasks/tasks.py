import dramatiq
import json
from cnninfer.storage import s3storage
from components.cnninfer.coco import api


@dramatiq.actor(store_results=True)
def hello(name: str) -> str:
    saved_string = f"Hello {name}"
    print(saved_string)
    return saved_string


@dramatiq.actor(store_results=True)
def prepare_coco_dataset(num_pictures: int) -> str:
    print(s3storage.create_bucket(s3storage.minio_client, "annotation"))
    print(s3storage.create_bucket(s3storage.minio_client, "preimages"))
    print(s3storage.create_bucket(s3storage.minio_client, "postimages"))

    # Upload COCO Dataset to Bucket
    coco_api = api.init_coco_api("./projects/inferengine/instances_val2017.json")
    img_ids = api.get_coco_image_ids(coco_api=coco_api, num_image=num_pictures, cat_names=None)
    coco_dataset = api.download_coco_images(coco_api=coco_api, img_ids=img_ids)

    for index, img in enumerate(coco_dataset.image_list):
        s3storage.upload_file_from_bytes(
            minio_client=s3storage.minio_client,
            bucket_name="preimages",
            object_name=coco_dataset.img_name_list[index],
            file_content=img,
            content_length=len(img)
        )

    return "Bucket Image Init Successful"


"""
@dramatiq.actor
def startEverything() -> None:
    download Files
    upload to s3 bucket
    submit each file for inference
    submit experiment data result per file
    """
