from ctypes import Union
import logging
import logging
import re
from typing import Any, Optional
from app.utils.resp import Resp, RespModel, RespUserModel
from app.models.database import get_session
from fastapi import Depends, Request, Body
from app.schema.user import UserResponse, UserSchema
from sqlalchemy.orm.session import Session
from starlette.responses import Response
from app.crud.user import UserDBActions
from app.models.user import User
from app.services.auth.auth_bearer import get_current_user
from app.utils.utils import convert_to

log = logging.getLogger(__name__)

class UserService:
    

    def __init__(self):
        self.user_db_actions = None


    
    #todo: remove additional fields
    async def fetch_user(self, request: Request, response: Response, \
                          db: Session = Depends(get_session),current_user: User = Depends(get_current_user), \
                            user_id: Optional[str | None] = None)-> RespUserModel:
        try:
            self.user_db_actions = UserDBActions(db,current_user)
            resp, msg = None,None

            if not user_id:
                if current_user.is_superuser():
                    # resp, msg = self.user_db_actions.fetch_user()
                    resp,msg = self.user_db_actions.fetch_user_by_id(current_user.id)
                else:
                    resp,msg = self.user_db_actions.fetch_user_by_id(current_user.id)
            else:
                if not len(user_id)>0:
                    response.status_code = 400
                    return RespUserModel(status=400,data="User id is empty")
                if current_user.is_superuser():
                    resp, msg =  self.user_db_actions.fetch_user_by_id(user_id)
                else:
                    if int(user_id) != current_user.id:
                        response.status_code = 401
                        return RespUserModel(status=401,data="You are not authorized to fetch the user")
                    print("")
                    resp, msg =  self.user_db_actions.fetch_user_by_id(user_id)
            if not resp:
                return RespUserModel(status=200,data=f"{msg}")
            data = convert_to(msg.dict(),UserResponse)
            return RespUserModel(status=200,data=data)
        except Exception as e:
            log.exception(f'Facing issue while fetching the new user  - {e}')
            response.status_code =  400
            return RespUserModel(status=400,data=f"{e}")


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