from __future__ import annotations

from datetime import timezone
from typing import BinaryIO

import boto3
from botocore.config import Config

from app.config import get_settings
from app.models.document import DocumentRecord


class S3Service:
    def __init__(self) -> None:
        settings = get_settings()
        self.bucket = settings.s3_bucket_name
        self.prefix = settings.s3_prefix
        self.client = boto3.client(
            "s3",
            region_name=settings.aws_region,
            aws_access_key_id=settings.aws_access_key or None,
            aws_secret_access_key=settings.aws_secret_key or None,
            config=Config(signature_version="s3v4"),
        )

    def _key_for_name(self, file_name: str) -> str:
        safe_name = file_name.replace("\\", "_").replace("/", "_")
        return f"{self.prefix}{safe_name}"

    def upload_file(self, file_name: str, file_stream: BinaryIO, content_type: str) -> str:
        key = self._key_for_name(file_name)
        self.client.upload_fileobj(
            Fileobj=file_stream,
            Bucket=self.bucket,
            Key=key,
            ExtraArgs={"ContentType": content_type},
        )
        return key

    def download_file_bytes(self, s3_key: str) -> bytes:
        response = self.client.get_object(Bucket=self.bucket, Key=s3_key)
        return response["Body"].read()

    def list_documents(self) -> list[DocumentRecord]:
        response = self.client.list_objects_v2(Bucket=self.bucket, Prefix=self.prefix)
        contents = response.get("Contents", [])
        documents: list[DocumentRecord] = []

        for item in contents:
            key = item["Key"]
            if key.endswith("/"):
                continue

            documents.append(
                DocumentRecord(
                    name=key.removeprefix(self.prefix),
                    size=item["Size"],
                    uploaded_at=item["LastModified"].astimezone(timezone.utc),
                    s3_key=key,
                )
            )

        documents.sort(key=lambda entry: entry.uploaded_at, reverse=True)
        return documents

