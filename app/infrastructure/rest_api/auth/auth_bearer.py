import datetime
import logging
from typing import List
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.infrastructure.rest_api.auth.auth_handler import decode_jwt

logger = logging.getLogger(__name__)

class JWTBearer(HTTPBearer):
    def __init__(self, roles:List[str], auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.roles_required = roles

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        logger.info("credentials: %s", str(credentials))

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")

            if not self.is_valid_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")

            if not self.contain_roles(credentials.credentials):
                raise HTTPException(status_code=401, detail="Invalid permissions.")

            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def is_valid_jwt(self, jwtoken: str):
        payload = decode_jwt(jwtoken)

        if not payload:
            return False

        is_token_valid: bool = False

        current_time = datetime.datetime.now(datetime.timezone.utc).timestamp()

        if payload["exp"] >= current_time:
            is_token_valid = True

        return is_token_valid

    def contain_roles(self, jwtoken):
        payload = decode_jwt(jwtoken)

        if not payload:
            return False

        is_token_valid: bool = False

        for rol in self.roles_required:
            if rol in payload["roles"]:
                is_token_valid = True

        return is_token_valid
