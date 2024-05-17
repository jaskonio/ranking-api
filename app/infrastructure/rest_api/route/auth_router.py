from fastapi import APIRouter

from app.infrastructure.rest_api.auth.auth_handler import UserAuthRequests, generate_guest_jwt, generate_jwt, user_is_valid

auth_router = APIRouter()

@auth_router.post('/')
def generate_token(user: UserAuthRequests):

    is_user_authenticated = user_is_valid(user)

    if not is_user_authenticated:
        return {"success": False}

    token_valid_user = generate_jwt(user)

    return token_valid_user

@auth_router.get('/guest')
def generate_token():

    token_valid_user = generate_guest_jwt()

    return token_valid_user
