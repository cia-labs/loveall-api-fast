import os
from fastapi.responses import HTMLResponse
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Response, status, Body, Depends
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.user import User
from app.schema.user import UserLoginSchema, UserRegister, UserSchema
from app.models.database import get_session
import logging
from app.crud.user import UserDBActions
from sqlalchemy.orm.session import Session
from app import Config, utils
from app.services.auth.auth_handler import decodeJWT, signJWT
from app.utils.resp import Resp
from app.utils.utils import pwd_context,post_to_n8n

log = logging.getLogger(__name__)

class AuthService:
    
    def __init__(self):
        self.auth_db_actions = None


    async def register(self,response:Response, user: UserRegister = Body(...), db: Session = Depends(get_session)):
        self.auth_db_actions = UserDBActions(db, User(
            name="", email=user.email, password=user.password, role="", is_active=0, created_by="",
            creation_time=datetime.now(),modification_time=datetime.now()))
        resp, msg = self.auth_db_actions.register_new_user(user)
        if resp:
            log.info(f'New user {user} saved successfully')
            found, userData =  self.auth_db_actions.fetch_user_by_email(email=user.email)
            if not found:
                log.error(f'User with email {user.email} is not found')
                return Resp.error(response, f'User with email {user.email} is not found')
            log.info(f'User with email {user.email} is found')
            gen_state, token = self.auth_db_actions.generate_activation_token(userData)
            if not gen_state:
                log.error(f'Facing issue while generating activation token for user - {msg}')
                return Resp.error(response, f'Facing issue while generating activation token for user - {msg}')
            log.info(f'Activation token generated successfully for user - {user.email}')
            n8n_state,n8n_response = post_to_n8n({"user_id":userData.id,"activation_base_link":"http://127.0.0.1:9000/auth/activate","email":user.email,"token":token})
            if not n8n_state:
                log.error(f'Facing issue while sending activation mail to user - {msg}')
                return Resp.error(response, f'Facing issue while sending activation mail to user - {msg}')
            log.info(f'Activation mail sent successfully to user - {user.email}')
            return Resp.success(response, msg)
        else:
            print(msg)
            log.error(f'Facing issue while saving the new user - {msg}')
            return Resp.error(response, msg)

    async def activate_user(self, response:Response,user_id: int, token: str, db: Session = Depends(get_session)):
        print("DEBIUG")
        self.auth_db_actions = UserDBActions(db, User(
            name="", email="", password="", role="", is_active=0, created_by="",
            creation_time=datetime.now(),modification_time=datetime.now()))
        resp, msg = self.auth_db_actions.verify_activation_token(user_id,token)
        htmlc= f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Page Title</title>
        </head>
        <body>
        <h1> {msg} </h1>
        </body>
        </html>
        '''        
        if not resp:
            log.error(f'Facing issue while verifying the activation token - {msg}')
            # return Resp.error(response, f'Facing issue while verifying the activation token - {msg}')
            return HTMLResponse(content=htmlc, status_code=400)
        log.info(f'Activation successful for user - {msg}')
        # return a html page saying token successful
        return HTMLResponse(content=htmlc, status_code=200)

    async def login(self, user: UserLoginSchema = Body(...), db: Session = Depends(get_session)):
        self.auth_db_actions = UserDBActions(db, User(
            name="", email=user.email, password=user.password, role="", is_active=0, created_by="",
            creation_time=datetime.now(),modification_time=datetime.now()))

        found, userData = self.auth_db_actions.fetch_user_by_email(user.email)
        log.debug(f"fetch user by email state: {found} resp: {userData}")
        if not found:
            raise HTTPException(status_code=404, detail="incorrect email or password")
        if not verify_password(user.password, userData.password):
            raise HTTPException(status_code=401, detail="invalid credentials")

        access_token_expires = timedelta(minutes=float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))) # type: ignore

        # Create a dictionary with the user fields you want to include in the JWT
        #TODO: fill in picture
        user_data_dict = {
            "name": userData.name,
            "email": userData.email,
            "picture":"",
            "role": userData.role.value,
            "is_active": userData.is_active
        }
   
        access_token,token_state = create_access_token(
            data={"sub": user_data_dict}, expires_delta=access_token_expires
        )
        if not token_state:
            return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token creation failed")

        return {"access_token": access_token, "token_type": "bearer"}

    async def authenticate_user(self, email: str, password: str):
        user = await User.get_by_email(email) # type: ignore
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
        return user

    # async def get_current_active_user(self, current_user: User = Depends(get_current_user)):
    #     if current_user.disabled:
    #         raise HTTPException(status_code=400, detail="Inactive user")
    #     return current_user

def verify_password(plain_password: str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt, sign_status = signJWT(to_encode)
    if not sign_status:
        return encoded_jwt, False
    return encoded_jwt, True

