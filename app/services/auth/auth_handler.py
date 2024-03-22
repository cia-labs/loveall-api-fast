import os
import time
from typing import Dict
from app import  Config
import jwt


def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, os.getenv("JWT_SECRET") , algorithm=os.getenv("JWT_ALGORITHM"))

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, os.getenv("JWT_SECRET") , algorithms=[os.getenv("JWT_ALGORITHM")])
        print(decoded_token)
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except:
        return {}
