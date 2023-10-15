import logging
from app.utils.logger import api_logger
from app.utils.resp import Resp
from app.models.database import get_session
from app.crud.store import StoreDBActions
from fastapi import Depends, Request, Body
from sqlalchemy.orm import Session
from starlette.responses import Response
from app.schema.store import StoreSchema
from app.models.user.user import User
from app.services.auth.auth_bearer import get_current_user


log = logging.getLogger(__name__)

class StoreService:
    method_decorators = [api_logger]

    def __init__(self):
        self.store_db_actions = None
    
    async def fetch_store(self, request: Request, response: Response, db: Session = Depends(get_session)):
        try:
            self.store_db_actions = StoreDBActions(db)
            resp, msg = self.store_db_actions.fetch_store_by_name("cdcdc")
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
            self.store_db_actions = StoreDBActions(db)
            resp, msg = self.store_db_actions.save_new_store(store,current_user.id)
            if resp:
                log.info(f'New store {store} saved successfully')
                return Resp.success(response, msg)
            else:
                log.error(f'Facing issue while saving the new store - {msg}')
                return Resp.error(response, msg)
        except Exception as e:
            log.exception(f'Facing issue while saving the new store - {e}')
            return Resp.error(response, f'Facing issue in store -{e}')
        
    async def update_store(self,store_id: str,response: Response, store: StoreSchema = Body(...),db: Session = Depends(get_session), current_user: User= Depends(get_current_user)):
        # todo : only user to update store details
        try:
            log.info(f'Updating store with the data - {store}')
            self.store_db_actions = StoreDBActions(db)
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