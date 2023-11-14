from minio import Minio
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
    secure=False
)

def create_bucket(minio_client: Minio, bucket_name: str) -> str:
    bucket_exist = minio_client.bucket_exists(bucket_name)
    if not bucket_exist:
        minio_client.make_bucket(bucket_name)
    
    return f"LOG - Bucket Exists: {bucket_name}"

#def upload_file_to_bucket_fd()

