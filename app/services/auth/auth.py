import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import HTTPException, status, Body, Depends
from app.models.user.user import User
from app.schema.user import UserLoginSchema
from app.models.database import get_session
from app.utils.logger import api_logger
# from app.config import settings
from app.crud.user import UserDBActions
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_SECRET = "please_please_update_me_please"
JWT_ALGORITHM = "HS256"

class AuthService:
    method_decorators = [api_logger]
    def __init__(self):
        self.auth_db_actions = None

    async def login (self, user:UserLoginSchema = Body(...) , db: Session = Depends(get_session)):
        self.auth_db_actions = UserDBActions(db)
        found,userData=self.auth_db_actions.fetch_user_by_email(user.email)
        print(found,userData)
        if not found:
            raise HTTPException(status_code=404, detail="User not found")
        if not verify_password(user.password, userData.password):
            raise HTTPException(status_code=401, detail="Incorrect password")
        # access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token_expires = timedelta(minutes=8600)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
        return {"msg":"yep"}
    

    async def authenticate_user(self, email: str, password: str):
        user = await User.get_by_email(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
        return user

    async def create_jwt_token(self, email: str, password: str):
        user = await self.authenticate_user(email, password)
        #TODO: fix from config
        # access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token_expires = timedelta(minutes=8600)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    # async def get_current_user(self, token: str = Depends(oauth2_scheme)):
    #     credentials_exception = HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Could not validate credentials",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    #     try:
    #         #TODO: fix from config
    #         # payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    #         payload = jwt.decode(token,"please_please_update_me_please","HS256" )
    #         email: str = payload.get("sub")
    #         if email is None:
    #             raise credentials_exception
    #     except JWTError:
    #         raise credentials_exception
    #     user = await User.get_by_email(email)
    #     if user is None:
    #         raise credentials_exception
    #     return user

    # async def get_current_active_user(self, current_user: User = Depends(get_current_user)):
    #     if current_user.disabled:
    #         raise HTTPException(status_code=400, detail="Inactive user")
    #     return current_user

def verify_password(plain_password, hashed_password):
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
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

# async def authenticate_user(email: str, password: str):
#     user = await User.get_by_email(email)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
#     if not verify_password(password, user.hashed_password):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
#     return user

# async def create_jwt_token(email: str, password: str):
#     user = await authenticate_user(email, password)
#     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.email}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}
