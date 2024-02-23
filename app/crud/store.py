import json
import uuid
from datetime import datetime
from app.models.user.user import User,Store
from app.schema.store import StoreSchema
from app.utils.logger import api_logger
import logging
from app.utils.utils import pwd_context

logger = logging.getLogger(__name__)

class StoreDBActions:
    method_decorators = [api_logger]

    def __init__(self, db,current_user: User):
        self.db = db
        self.current_user = current_user

    def fetch_store(self):
        """
        Fetch store
        :return: True if success else False
        """
        try:
            stores=None
            if self.current_user.is_superuser():
                logger.info(f'User is superuser')
                stores = self.db.query(Store).all()
            else:
                stores = self.db.query(Store).all()
            if stores:
                return True, stores
            return False, f'Store not found'
        except Exception as e:
            logger.exception(f'Facing issue while fetching the store - {e}')
            return False, f'Facing issue while fetching the store'

    def fetch_store_by_id(self, id: int):
        """
        Fetch store by name
        :param name: Name of the store
        :return: True if success else False
        """
        try:
            stores=None
            if self.current_user.is_superuser():
                logger.info(f'User is superuser')
                stores = self.db.query(Store).filter(Store.id == id).all()
            else:
                logger.info(f'User is not a superuser {self.current_user.id}')
                stores = self.db.query(Store).filter(Store.id == id).filter(Store.user_id==self.current_user.id).all()
            if stores:
                return True, stores
            return False, f'Store with name {id} not found'
        except Exception as e:
            logger.exception(f'Facing issue while fetching the store with name {id} - {e}')
            return False, f'Facing issue while fetching the store with name {id}'
        
    def save_new_store(self, store: StoreSchema):
        """
        Save new store
        :param store: New store details
        :return: True if success else False
        """
        try:

            print(self.current_user.email)
            self.db.add(Store(**store.dict(),**{
                "user_id": self.current_user.id,
                "creation_time":datetime.now(),
                "modification_time": datetime.now(),
                "created_by" :self.current_user.email
            }))
            self.db.commit()
            return True, f'Store {store} saved successfully'
        except Exception as e:
            logger.exception(f'Facing issue while saving the new store - {e}')
            return False, f'Facing issue while saving the new store - {e}'
    
    def update_store(self, store: StoreSchema,store_id: str):
        """
        Update store
        :param store: Store details
        :return: True if success else False
        """
        try:
            result = None
            final_update = {**store.dict(),**{
                    "modification_time": str(datetime.now()),
                }}
            logger.info(f'User is superuser {self.current_user.is_superuser()} -- {self.current_user.email} -- {self.current_user.role}')
            print(final_update)
            if self.current_user.is_superuser():
                logger.info(f'User is superuser')
                # add modification time to store.dict()
                
                result = self.db.query(Store).filter(Store.id == store_id).update(final_update)
            else:
                result = self.db.query(Store).filter(Store.id == store_id,Store.user_id==self.current_user.id).update(final_update)
            if result == 0:
                return False, f'Store with id {store_id} not found for user'
            self.db.commit()
            return True, f'Store {store} updated successfully'
        except Exception as e:
            logger.exception(f'Facing issue while updating the store - {e}')
            return False, f'Facing issue while updating the store - {e}'