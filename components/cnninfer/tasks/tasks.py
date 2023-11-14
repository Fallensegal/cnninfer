import dramatiq
from cnninfer.storage import s3storage


@dramatiq.actor(store_results=True)
def hello(name: str) -> str:
    saved_string = f"Hello {name}"
    print(saved_string)
    return saved_string


@dramatiq.actor(store_results=True)
def prepare_coco_dataset() -> str:
    print(s3storage.create_bucket(s3storage.minio_client, "annotation"))
    print(s3storage.create_bucket(s3storage.minio_client, "images"))

    # Put Annotation in S3 Bucket:
    s3storage.upload_file_from_fs(
        s3storage.minio_client,
        "annotation",
        "instances_val17.json",
        "./projects/inferengine/instances_val2017.json",
    )

    return "Bucket Init Successful"


"""
@dramatiq.actor
def startEverything() -> None:
    download Files
    upload to s3 bucket
    submit each file for inference
    submit experiment data result per file
    """
