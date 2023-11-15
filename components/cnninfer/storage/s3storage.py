from minio import Minio
from io import BytesIO
import requests
from pydantic import SecretStr, BaseModel
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    minio_user: str
    minio_password: SecretStr


settings = Settings()

minio_client = Minio(
    "chart-minio:9000",
    access_key=settings.minio_user,
    secret_key=settings.minio_password.get_secret_value(),
    secure=False,
)


def create_bucket(minio_client: Minio, bucket_name: str) -> str:
    bucket_exist = minio_client.bucket_exists(bucket_name)
    if not bucket_exist:
        minio_client.make_bucket(bucket_name)
        return f"Success - Created Bucket: {bucket_name}"
    return f"LOG - Bucket Exists: {bucket_name}"


def upload_file_from_bytes(
    minio_client: Minio,
    bucket_name: str,
    object_name: str,
    file_content: bytes,
    content_length: int,
) -> None:
    minio_client.put_object(
        bucket_name=bucket_name,
        object_name=object_name,
        data=BytesIO(file_content),
        length=content_length,
        content_type="application/octet-stream",
    )


def upload_file_from_fs(
    minio_client: Minio, bucket_name: str, obj_name: str, file_path: str
) -> None:
    minio_client.fput_object(bucket_name, obj_name, file_path)


def download_file_from_bucket(
    minio_client: Minio, bucket_name: str, object_name: str
) -> None:
    ...


# def upload_file_to_bucket_fd()
