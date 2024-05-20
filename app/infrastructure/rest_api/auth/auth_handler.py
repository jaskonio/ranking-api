import datetime
from enum import Enum
import logging
from typing import Dict, List
import jwt
from pydantic import BaseModel# [import-error]
from app.core.config import Settings

logger = logging.getLogger(__name__)

class UserAuthModel(BaseModel):
    user_name: str
    password: str
    roles: List[str]

class UserAuthRequests(BaseModel):
    user_name: str
    password: str

class Roles(str, Enum):
    VIEW = "view"
    ADMIN = "admin"

class UserDBService():
    db_users:List[UserAuthModel] = []

    guest_user = UserAuthModel(user_name=Settings.AUTH_GUEST_USER, password=Settings.AUTH_GUEST_PASSWORD, roles=Settings.AUTH_GUEST_ROLES)

    def __init__(self) -> None:
        self.db_users.append(UserAuthModel(user_name=Settings.AUTH_ADMIN_USER, password=Settings.AUTH_ADMIN_PASSWORD, roles=Settings.AUTH_ADMIN_ROLES))
        self.db_users.append(self.guest_user)

    def getUserByName(self, user:UserAuthRequests):
        for db_user in self.db_users:
            if db_user.user_name == user.user_name and db_user.password == user.password:
                return db_user

        return None

user_db_service = UserDBService()

def user_is_valid(user:UserAuthRequests):
    user_exist_in_db = user_db_service.getUserByName(user)

    if user_exist_in_db is None or not user_exist_in_db:
        return False

    return True

def generate_jwt(user: UserAuthRequests) -> Dict[str, str]:
    db_user = user_db_service.getUserByName(user)
    time = datetime.datetime.now(datetime.timezone.utc)
    time_expired = time + datetime.timedelta(minutes=Settings.AUTH_ACCESS_TOKEN_EXPIRE_MINUTES)

    time_epoch = int(time.timestamp())
    time_expired_epoch = int(time_expired.timestamp())
       
    payload = {
        "iat": time_epoch,
        "exp": time_expired_epoch,
        "user_name": db_user.user_name
    }

    token = jwt.encode(payload, Settings.AUTH_SECRET_KEY, algorithm=Settings.AUTH_ALGORITHM)

    token_response = {
        "access_token": token,
        "expires_in": time_expired_epoch,
        "token_type": "bearer",
        "roles": db_user.roles,
        "success": True
    }

    return token_response

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

def generate_guest_jwt():
    return generate_jwt(UserDBService.guest_user)
