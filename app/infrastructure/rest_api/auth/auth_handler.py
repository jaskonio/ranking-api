import datetime
import logging
from typing import Dict
import os
from fastapi import Depends, HTTPException, status
import jwt
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.core.config import Settings

logger = logging.getLogger(__name__)

class UserAuthModel(BaseModel):
    user_name: str
    password: str

def user_is_valid(user:UserAuthModel):
    return user.user_name == Settings.AUTH_USER and user.password == Settings.AUTH_PASSWORD

def token_response(token: str):
    return {
        "access_token": token,
        "token_type": "bearer"
    }

def generate_jwt(user: UserAuthModel) -> Dict[str, str]:
    time = datetime.datetime.now(datetime.timezone.utc)
    payload = {
        "iat": time,
        "exp": time + datetime.timedelta(minutes=Settings.AUTH_ACCESS_TOKEN_EXPIRE_MINUTES),
        "user_name": user.user_name
    }

    token = jwt.encode(payload, Settings.AUTH_SECRET_KEY, algorithm=Settings.AUTH_ALGORITHM)

    return token_response(token)

def decode_jwt(token: str):
    try:
        decoded_token = jwt.decode(token, Settings.AUTH_SECRET_KEY, algorithms=[Settings.AUTH_ALGORITHM])
        logger.info("decoded_token: %s", str(decoded_token))

        return decoded_token
    except Exception as exception_error:
        logger.error(exception_error)
        return None

def is_valid_jwt(jwtoken: str):
    payload = decode_jwt(jwtoken)

    if not payload:
        return False

    is_token_valid: bool = False

    current_time = datetime.datetime.now(datetime.timezone.utc).timestamp()
    logger.info("current_time: %s", str(current_time))

    if payload["expires"] >= current_time:
        is_token_valid = True

    return is_token_valid
