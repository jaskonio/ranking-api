"""_summary_

Returns:
    _type_: _description_
"""
import logging
from typing import Dict
import os
import time
import jwt

from app.model.user_model import UserModel

logger = logging.getLogger(__name__)

JWT_SECRET = os.getenv("JWT_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

USER_ADMIN = os.getenv("USER_ADMIN")
PASSWORD_ADMIN = os.getenv("PASSWORD_ADMIN")


def user_is_valid(user:UserModel):
    """_summary_

    Args:
        user (UserModel): _description_

    Returns:
        _type_: _description_
    """
    return user.user_name == USER_ADMIN and user.password == PASSWORD_ADMIN

def token_response(token: str):
    """_summary_

    Args:
        token (str): _description_

    Returns:
        _type_: _description_
    """
    return {
        "access_token": token
    }

def sign_jwt(user: UserModel) -> Dict[str, str]:
    """_summary_

    Returns:
        _type_: _description_
    """
    payload = {
        "user_name": user.user_name,
        "expires": time.time() + 600
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)

def decode_jwt(token: str):
    """_summary_

    Args:
        token (str): _description_

    Returns:
        _type_: _description_
    """
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        logger.info("decoded_token: %s", str(decoded_token))

        if decoded_token["expires"] >= time.time():
            decoded_token = None

        return decoded_token
    except:
        return {}
