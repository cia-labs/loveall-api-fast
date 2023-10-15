import logging
from app.utils.logger import api_logger
from app.utils.resp import Resp
from app.models.database import get_session
from fastapi import Depends, Request
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

    async def fetch_user(self, request: Request, response: Response, db: Session = Depends(get_session),current_user: User = Depends(get_current_user)):
        try:
            print("CurrentUser",current_user.name)
            # data = await request.json()
            # payload_as_json= request.json()
            # params = await request.body()
            # if params:
            #     log.info(params)
            # log.info(params)

            # print("data",payload_as_json)
            # log.info(f'1Fetching the user with the name - {data}')
            
            # log.info(f'Fetching the user with the name - {data.get("name")}')
            self.user_db_actions = UserDBActions(db)
            
            # resp, msg = self.user_db_actions.fetch_user_by_name(data.get('name'))
            data={"name":""}
            resp, msg = self.user_db_actions.fetch_user_by_name("cdcdc")
            if resp:
                log.info(f'User fetched successfully with the name: {data.get("name")}')
                return Resp.success(response, msg)
            else:
                log.error(f'Facing issue while fetching the new user {data.get("name")} - {msg}')
                return Resp.error(response, msg)
        except Exception as e:
            # log.exception(f'Facing issue while fetching the new user {data.get("name")} - {e}')
            log.exception(f'Facing issue while fetching the new user  - {e}')
            return Resp.error(response, f'Facing issue in user -{e}')


    async def create_user(self, request: Request, response: Response, db: Session = Depends(get_session)):
        try:
            data = await request.json()
            log.info(f'Creating new user with the data - {data}')
            self.user_db_actions = UserDBActions(db)
            resp, msg = self.user_db_actions.save_new_user(data)
            if resp:
                log.info(f'New user {data.get("name")} saved successfully')
                return Resp.success(response, msg)
            else:
                print(msg)
                log.error(f'Facing issue while saving the new user {data.get("name")} - {msg}')
                return Resp.error(response, msg)
        except Exception as e:
            log.exception(f'Facing issue while saving the new user {data.get("name")} - {e}')
            print(e)
            return Resp.error(response, f'Facing issue in user -{e}')