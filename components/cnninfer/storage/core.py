from minio import Minio
from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    minio_user: str
    minio_password: SecretStr


settings = Settings()

minioClient = Minio(
    "chart-minio.default.svc.cluster.local",
    access_key=settings.minio_user,
    secret_key=settings.minio_password.get_secret_value(),
)

found = minioClient.bucket_exists("images")
if not found:
    minioClient.make_bucket("images")

