"""_summary_

Raises:
    HTTPException: _description_
    HTTPException: _description_
    HTTPException: _description_

Returns:
    _type_: _description_
"""
import datetime
import logging
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.auth_handler import decode_jwt

logger = logging.getLogger(__name__)

class JWTBearer(HTTPBearer):
    """_summary_

    Args:
        HTTPBearer (_type_): _description_
    """
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        logger.info("credentials: %s", str(credentials))

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str):
        """_summary_

        Returns:
            _type_: _description_
        """
        is_token_valid: bool = False

        payload = decode_jwt(jwtoken)

        if not payload:
            return False

        current_time = datetime.datetime.now(datetime.timezone.utc).timestamp()
        logger.info("current_time: %s", str(current_time))

        if payload["expires"] >= current_time:
            is_token_valid = True

        return is_token_valid
