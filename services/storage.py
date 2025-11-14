# Location: datanex/services/storage.py

from minio import Minio
from minio.error import S3Error
from utils.config import get_settings
from utils.logger import log
from io import BytesIO
from typing import Optional
import uuid

settings = get_settings()

class StorageService:
    def __init__(self):
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE
        )
        self.bucket = settings.MINIO_BUCKET
        self._ensure_bucket()
    
    def _ensure_bucket(self):
        try:
            if not self.client.bucket_exists(self.bucket):
                self.client.make_bucket(self.bucket)
                log.info(f"Created bucket: {self.bucket}")
        except S3Error as e:
            log.error(f"Error creating bucket: {e}")
            raise
    
    async def upload_file(self, file_data: bytes, filename: str, content_type: str) -> str:
        try:
            file_id = str(uuid.uuid4())
            object_name = f"{file_id}/{filename}"
            
            self.client.put_object(
                self.bucket,
                object_name,
                BytesIO(file_data),
                length=len(file_data),
                content_type=content_type
            )
            
            log.info(f"Uploaded file: {object_name}")
            return object_name
            
        except S3Error as e:
            log.error(f"Error uploading file: {e}")
            raise
    
    async def download_file(self, object_name: str) -> bytes:
        try:
            response = self.client.get_object(self.bucket, object_name)
            data = response.read()
            response.close()
            response.release_conn()
            return data
        except S3Error as e:
            log.error(f"Error downloading file: {e}")
            raise
    
    async def delete_file(self, object_name: str) -> bool:
        try:
            self.client.remove_object(self.bucket, object_name)
            log.info(f"Deleted file: {object_name}")
            return True
        except S3Error as e:
            log.error(f"Error deleting file: {e}")
            return False
    
    async def get_file_url(self, object_name: str, expiry: int = 3600) -> str:
        try:
            url = self.client.presigned_get_object(
                self.bucket,
                object_name,
                expires=expiry
            )
            return url
        except S3Error as e:
            log.error(f"Error generating URL: {e}")
            raise

storage_service = StorageService()