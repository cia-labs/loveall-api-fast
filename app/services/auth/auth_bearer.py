from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .auth_handler import decodeJWT
from fastapi import FastAPI, Body, Depends
from app.models.database import get_session
from sqlalchemy.orm.session import Session
from app.models.user import User
import json


def get_current_user(token: str,db: Session = Depends(get_session)):
    decodedData,state = decodeJWT(token)
    details = decodedData["sub"]
    user_data = db.query(User).filter(User.email == details.get("email")).first() # type: ignore
    return  user_data