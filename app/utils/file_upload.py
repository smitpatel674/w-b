import boto3
import os
from typing import Optional
from fastapi import UploadFile
from app.core.config import settings


class S3Uploader:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region
        )
        self.bucket_name = settings.aws_s3_bucket

    def upload_file(self, file: UploadFile, folder: str = "uploads") -> Optional[str]:
        """Upload file to S3 and return the URL"""
        try:
            # Generate unique filename
            file_extension = os.path.splitext(file.filename)[1]
            unique_filename = f"{folder}/{os.urandom(16).hex()}{file_extension}"
            
            # Upload to S3
            self.s3_client.upload_fileobj(
                file.file,
                self.bucket_name,
                unique_filename,
                ExtraArgs={
                    'ContentType': file.content_type,
                    'ACL': 'public-read'
                }
            )
            
            # Return the public URL
            return f"https://{self.bucket_name}.s3.{settings.aws_region}.amazonaws.com/{unique_filename}"
        
        except Exception as e:
            print(f"Error uploading file to S3: {e}")
            return None

    def delete_file(self, file_url: str) -> bool:
        """Delete file from S3"""
        try:
            # Extract key from URL
            key = file_url.split(f"{self.bucket_name}.s3.{settings.aws_region}.amazonaws.com/")[1]
            
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=key
            )
            return True
        
        except Exception as e:
            print(f"Error deleting file from S3: {e}")
            return False


# Global S3 uploader instance
s3_uploader = S3Uploader()


def upload_course_thumbnail(file: UploadFile) -> Optional[str]:
    """Upload course thumbnail image"""
    return s3_uploader.upload_file(file, "course-thumbnails")


def upload_course_video(file: UploadFile) -> Optional[str]:
    """Upload course video file"""
    return s3_uploader.upload_file(file, "course-videos")


def upload_user_avatar(file: UploadFile) -> Optional[str]:
    """Upload user profile avatar"""
    return s3_uploader.upload_file(file, "user-avatars")


def upload_lesson_material(file: UploadFile) -> Optional[str]:
    """Upload lesson material file"""
    return s3_uploader.upload_file(file, "lesson-materials")
