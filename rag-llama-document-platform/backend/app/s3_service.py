import os
from pathlib import Path
from io import BytesIO

import boto3
from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parents[1] / ".env")


s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

BUCKET = os.getenv("S3_BUCKET_NAME", "lama-s3-rag12345678")


def upload_to_s3(file_obj, filename: str) -> None:
    s3.upload_fileobj(file_obj, BUCKET, filename)


def upload_bytes_to_s3(file_bytes: bytes, filename: str) -> None:
    s3.upload_fileobj(BytesIO(file_bytes), BUCKET, filename)


def download_from_s3(filename: str, local_path: str) -> None:
    s3.download_file(BUCKET, filename, local_path)


def list_s3_files() -> list[dict[str, str | int]]:
    response = s3.list_objects_v2(Bucket=BUCKET)
    files: list[dict[str, str | int]] = []

    for obj in response.get("Contents", []):
        files.append(
            {
                "name": obj["Key"],
                "size": obj["Size"],
                "uploaded_at": obj["LastModified"].isoformat(),
            }
        )

    return files
