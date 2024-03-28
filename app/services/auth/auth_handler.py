from math import log
import os
import time
from typing import Dict, Union
from app import  Config
import jwt
import logging

log = logging.getLogger(__name__)


def token_response(token: str):
    return {
        "access_token": token
    }

def signJWT(payload: dict):
    try:
        token = jwt.encode(payload, os.getenv("JWT_SECRET"), algorithm=os.getenv("JWT_ALGORITHM")) # type: ignore
        return token,True
    except Exception as e:
        log.debug(f"Error signing token: {e}")
        return {"error": f"{e}"},False

def decodeJWT(token: str):
    try:
        decoded_token = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=[os.getenv("JWT_ALGORITHM")]) # type: ignore
        if not decoded_token["exp"] >= time.time():
            return {},False
        return decoded_token,True
    except Exception as e:
        log.debug(f"Error decoding token: {e}")
        return {"failed":f"{e}"},False
