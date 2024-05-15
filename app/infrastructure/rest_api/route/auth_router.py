from fastapi import APIRouter

from app.infrastructure.rest_api.auth.auth_handler import UserAuthModel, generate_jwt, user_is_valid

auth_router = APIRouter()

@auth_router.post('/')
def generate_token(user: UserAuthModel):

    is_user_authenticated = user_is_valid(user)

    if not is_user_authenticated:
        return {"success": False}

    token_valid_user = generate_jwt(user)

    return token_valid_user
