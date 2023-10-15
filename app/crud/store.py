import json
import uuid
from datetime import datetime

from app.models.user.user import User,Store
from app.schema.store import StoreSchema
from app.utils.logger import api_logger
import logging


from passlib.context import CryptContext

logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class StoreDBActions:
    method_decorators = [api_logger]

    def __init__(self, db):
        self.db = db
    
    def fetch_store_by_name(self, name: str):
        """
        Fetch store by name
        :param name: Name of the store
        :return: True if success else False
        """
        try:
            stores = self.db.query(Store).filter(Store.name == name).all()
            if stores:
                return True, stores
            return False, f'Store with name {name} not found'
        except Exception as e:
            logger.exception(f'Facing issue while fetching the store with name {name} - {e}')
            return False, f'Facing issue while fetching the store with name {name}'

    def save_new_store(self, store: StoreSchema,user_id:int):
        """
        Save new store
        :param store: New store details
        :return: True if success else False
        """
        try:

            # StoreSchema(**store)
            print(store)
            print(user_id)
            self.db.add(Store(**store.dict(),**{
                "user_id": user_id,
                "creation_time":datetime.now(),
                "modification_time": datetime.now(),
                "created_by" :""
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
            # todo : handle errors
            self.db.query(Store).filter(Store.id == store_id).update(store.dict())
            self.db.commit()
            return True, f'Store {store} updated successfully'
        except Exception as e:
            logger.exception(f'Facing issue while updating the store - {e}')
            return False, f'Facing issue while updating the store - {e}'