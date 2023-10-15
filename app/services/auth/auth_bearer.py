from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .auth_handler import decodeJWT
from fastapi import FastAPI, Body, Depends
from app.models.database import get_session
from sqlalchemy.orm import Session
from app.models.user.user import User


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False
        try:
            payload = decodeJWT(jwtoken)
            print(payload)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid


def get_current_user(token: str = Depends(JWTBearer()),db: Session = Depends(get_session)):
    decodedData = decodeJWT(token)
    user_data = db.query(User).filter(User.email == decodedData.get("sub")).first()
    return  user_data