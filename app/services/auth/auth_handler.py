from math import log
import os
import time
from typing import Dict
from app import  Config
import jwt
import logging

log = logging.getLogger(__name__)


def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, os.getenv("JWT_SECRET"), algorithm=os.getenv("JWT_ALGORITHM")) # type: ignore
    

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        print("before",token)
        print("before",type(token))
        print("vars: ",os.getenv("JWT_SECRET"),os.getenv("JWT_ALGORITHM"),os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

        decoded_token = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=[os.getenv("JWT_ALGORITHM")]) # type: ignore
        print("after",decoded_token)
        print(decoded_token)
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except Exception as e:
        print(e)
        log.debug(f"Error decoding token: {e}")
        return {}
