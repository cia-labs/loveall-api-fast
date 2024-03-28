import logging
from app.models.storage import Storage
from app.models.user import User
import logging

logger = logging.getLogger(__name__)



class StorageDBActions:
    

    def __init__(self, db,current_user: User):
        self.db = db
        self.current_user = current_user

    def save_uploaded_info(self,filename:str,bucket_name:str,meta_data:dict={}):
        """
        Save uploaded info
        :return: True if success else False
        """
        try:
            print("saving: ",filename,bucket_name,meta_data)
            self.db.add(Storage(
                user_id=self.current_user.id,
                filename=filename,
                bucket=bucket_name,
                meta_data=meta_data
            ))
            self.db.commit()
            return True, "Uploaded info saved successfully"
        except Exception as e:
            logger.exception(f'Facing issue while saving the uploaded info - {e}')
            return False, f'Facing issue while saving the uploaded info'
