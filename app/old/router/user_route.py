"""_summary_

Returns:
    _type_: _description_
"""
from fastapi import APIRouter, HTTPException
from app.auth.auth_handler import sign_jwt, user_is_valid
from app.model.user_model import UserModel

user_router = APIRouter()

@user_router.post('/signup')
def signup(user: UserModel):
    """_summary_

    Args:
        user (UserModel): _description_

    Returns:
        _type_: _description_
    """
    if not user_is_valid(user):
        raise HTTPException(status_code=401, detail="Invalid user or password.")

    return sign_jwt(user)
    