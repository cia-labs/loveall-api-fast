import logging
from app.utils.logger import api_logger
from app.utils.resp import Resp
from app.models.database import get_session
from fastapi import Depends, Request, Body
from app.schema.user import UserSchema
from sqlalchemy.orm import Session
from starlette.responses import Response
from app.crud.user import UserDBActions
from app.models.user.user import User
from app.services.auth.auth_bearer import JWTBearer,get_current_user

log = logging.getLogger(__name__)

class UserService:
    method_decorators = [api_logger]

    def __init__(self):
        self.user_db_actions = None

    #todo: remove additional fields
    async def fetch_user(self,user_id: str, request: Request, response: Response, db: Session = Depends(get_session),current_user: User = Depends(get_current_user)):
        try:
            self.user_db_actions = UserDBActions(db,current_user)
            resp, msg = None,None
            if user_id and len(user_id)>0:
                resp, msg =  self.user_db_actions.fetch_user_by_id(user_id)
            else:
                resp, msg = self.user_db_actions.fetch_user()
            if resp:
                log.info(f'User fetched successfully with the name:')
                # return response without user password key
                return Resp.success(response, msg)
            else:
                log.error(f'Facing issue while fetching the new user  {msg}')
                return Resp.error(response, msg)
        except Exception as e:
            # log.exception(f'Facing issue while fetching the new user {data.get("name")} - {e}')
            log.exception(f'Facing issue while fetching the new user  - {e}')
            return Resp.error(response, f'Facing issue in user -{e}')


    async def create_user(self,response: Response, user: UserSchema = Body(...),db: Session = Depends(get_session), current_user: User= Depends(get_current_user)):
        try:
            log.info(f'Creating new user with the data - ')
            self.user_db_actions = UserDBActions(db,current_user)
            resp, msg = self.user_db_actions.save_new_user(user)
            if resp:
                log.info(f'New user {user} saved successfully')
                return Resp.success(response, msg)
            else:
                print(msg)
                log.error(f'Facing issue while saving the new user - {msg}')
                return Resp.error(response, msg)
        except Exception as e:
            log.exception(f'Facing issue while saving the new user - {e}')
            print(e)
            return Resp.error(response, f'Facing issue in user -{e}')