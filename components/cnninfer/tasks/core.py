import dramatiq
from minio import Minio
from components.cnninfer.storage import core

@dramatiq.actor(store_results=True)
def hello(name:str) -> str:
    saved_string = f'Hello {name}'
    print(saved_string)
    return saved_string

@dramatiq.actor(store_results=True)
def prepare_inference_experiment() -> str:
    core.create_bucket(core.minio_client, "annotation")
    return "Success - Created Bucket: annotation"

"""
@dramatiq.actor
def startEverything() -> None:
    download Files
    upload to s3 bucket
    submit each file for inference
    submit experiment data result per file
    """