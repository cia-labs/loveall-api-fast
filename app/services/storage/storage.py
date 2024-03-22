import io
import logging
import os
from typing import List
import uuid

from app.crud.storage import StorageDBActions
from app.models.database import get_session
from app.models.user.user import User
from app.services.auth.auth_bearer import get_current_user
from app.utils.logger import api_logger
from fastapi import Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.utils.utils import MINIO_BUCKET_NAME, minio_client


log = logging.getLogger(__name__)

class StorageService:
    method_decorators = [api_logger]

    def __init__(self):
        self.storage_db_actions = None
    
    def is_supported_format(self,filename: str) -> bool:
        """
        Checks if the given filename has a supported file format.

        Parameters:
            filename (str): Name of the file.

        Returns:
            bool: True if the file format is supported, False otherwise.
        """
        SUPPORTED_FORMATS = [".jpg", ".jpeg", ".png"]
        ext = os.path.splitext(filename)[1]
        return ext.lower() in SUPPORTED_FORMATS

    async def upload_file(self, files: List[UploadFile] = File(...), db: Session = Depends(get_session), current_user: User= Depends(get_current_user)):
        self.storage_db_actions = StorageDBActions(db,current_user)
        print("DEBUGGI")
        """
        Upload file
        """
        uploaded_files = []
        try:
            for file in files:
                unique_filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
                file_bytes = await file.read()
                result = minio_client.put_object(MINIO_BUCKET_NAME,unique_filename, io.BytesIO(file_bytes), len(file_bytes))
                log.info(f"created {result.object_name} object; etag: {result.etag}, version-id: {result.version_id}")
                self.storage_db_actions.save_uploaded_info(unique_filename,MINIO_BUCKET_NAME)
                uploaded_files.append(unique_filename)
                log.info(f"Uploaded {unique_filename} to MinIO")
            return {"message": "Files uploaded successfully@!"}
        except Exception as e:
            # Rollback by deleting uploaded files
            for uploaded_file in uploaded_files:
                minio_client.remove_object(MINIO_BUCKET_NAME, uploaded_file)
            raise HTTPException(status_code=500, detail="An unexpected error occurred. Rolled back.")