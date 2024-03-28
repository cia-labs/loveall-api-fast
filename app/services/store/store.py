
import io
import logging
import os
from typing import List
import uuid

from sqlalchemy import func
from app.crud.storage import StorageDBActions
from app.models.storage import Storage
import logging
from app.utils.resp import Resp
from app.utils.utils import MINIO_BUCKET_NAME, minio_client
from app.models.database import get_session
from app.crud.store import StoreDBActions
from fastapi import Depends, File, Request, Body, UploadFile
from sqlalchemy.orm import Session
from starlette.responses import Response
from app.schema.store import StoreSchema
from app.models.user import User
from app.services.auth.auth_bearer import get_current_user


log = logging.getLogger(__name__)

class StoreService:
    

    def __init__(self):
        self.store_db_actions = None
    
    async def fetch_store(self,store_id:str,request: Request, response: Response, db: Session = Depends(get_session),current_user: User= Depends(get_current_user)):
        try:

            self.store_db_actions = StoreDBActions(db,current_user)
            resp, msg = None,None
            if store_id and len(store_id)>0:
                resp, msg =  self.store_db_actions.fetch_store_by_id(store_id)
            else:
                resp, msg = self.store_db_actions.fetch_store()
            if resp:
                log.info(f'Store fetched successfully with the name: ')
                return Resp.success(response, msg)
            else:
                log.error(f'Facing issue while fetching the new store  - {msg}')
                return Resp.error(response, msg)
        except Exception as e:
            # log.exception(f'Facing issue while fetching the new user {data.get("name")} - {e}')
            log.exception(f'Facing issue while fetching the new store  - {e}')
            return Resp.error(response, f'Facing issue in store -{e}')
    
        
    
    async def create_store(self,response: Response, store: StoreSchema = Body(...),db: Session = Depends(get_session), current_user: User= Depends(get_current_user)):
        try:
        
            log.info(f'Creating new store with the data - {store}')
            self.store_db_actions = StoreDBActions(db,current_user=current_user)
            resp, msg = self.store_db_actions.save_new_store(store)
            if resp:
                log.info(f'New store {store} saved successfully')
                return Resp.success(response, msg)
            else:
                log.error(f'Facing issue while saving the new store - {msg}')
                return Resp.error(response, msg)
        except Exception as e:
            log.exception(f'Facing issue while saving the new store - {e}')
            return Resp.error(response, f'Facing issue in store -{e}')

    async def update_store(self,store_id: str,response: Response, store: dict = Body(...),db: Session = Depends(get_session), current_user: User= Depends(get_current_user)):
        # todo : only user to update store details
        try:
            if not store_id or len(store_id) == 0:
                log.error(f'No store id provided')
                return Resp.error(response, f'No store id provided')
            log.info(f'Updating store with the data - {store}')
            self.store_db_actions = StoreDBActions(db,current_user)
            resp, msg = self.store_db_actions.update_store(store,store_id)
            if resp:
                log.info(f'Store {store} updated successfully')
                return Resp.success(response, msg)
            else:
                log.error(f'Facing issue while updating the store - {msg}')
                return Resp.error(response, msg)
        except Exception as e:
            log.exception(f'Facing issue while updating the store - {e}')
            return Resp.error(response, f'Facing issue in store -{e}')
        
    async def upload_store_image(self, store_id: int, images_key: str, response: Response, files: List[UploadFile] = File(...),db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
        uploaded_files = []
        try:
            log.info(f'Uploading image for store {store_id}')
            self.store_db_actions = StoreDBActions(db,current_user)
            storage_db_actions = StorageDBActions(db,current_user)
            for file in files:
                unique_filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
                file_bytes = await file.read()
                result = minio_client.put_object(
                    MINIO_BUCKET_NAME,unique_filename, io.BytesIO(file_bytes), len(file_bytes),
                )
                log.info(f'Created {unique_filename} object; etag: {result.etag}, version-id: {result.version_id}')
                storage_db_actions.save_uploaded_info(unique_filename,MINIO_BUCKET_NAME) # type: ignore
                uploaded_files.append(unique_filename)
                log.info(f"Uploaded {unique_filename} to MinIO")
                fetch_state, fetch_store = self.store_db_actions.fetch_store_by_id(store_id)
                if fetch_state:
                    cur_meta_data = fetch_store[0].dict().get("meta_data")
                    if images_key == "primary":
                        cur_meta_data["images"]["primary"] = {
                            "name" : unique_filename,
                            "bucket" : MINIO_BUCKET_NAME
                        }
                    if images_key == "secondary":
                        cur_meta_data["images"]["secondary"].append({
                            "name" : unique_filename,
                            "bucket" : MINIO_BUCKET_NAME
                        })
                    self.store_db_actions.update_meta_data(int(store_id),cur_meta_data)
                else:
                    #TOOD: failed -  handle pass
                    pass
            return Resp.success(response, "Image uploaded successfully for store")
        except Exception as e:
            log.exception(f'Facing issue while uploading image for store {store_id} - {e}')
            return Resp.error(response, f'Facing issue while uploading image  -{e}')