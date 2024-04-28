import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import Settings
from app.infrastructure.rest_api.route.import_routers import get_routers
from app.infrastructure.rest_api.model.custom_responses import ErrorJsonResponse, FailJsonResponse


logger = logging.getLogger(__name__)

def add_middleware(fast_api: FastAPI):
    origins = ["*"]

    fast_api.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

custom_responses = {
    # 200: {
    #     "model": SuccessJsonPersonResponse,
    # },
    400: {
        "model": FailJsonResponse,
        "description": "Fail requests"
        },
    404: {
        "model": FailJsonResponse,
        "description": "Item not found"
        },
    500: {
        "model":ErrorJsonResponse,
        "description": "Internal Server Error"
        },
}

def start_application():
    fast_api = FastAPI(
        title=Settings.PROJECT_NAME,
        version=Settings.PROJECT_VERSION,
        responses=custom_responses)

    logging.info("include_router")
    fast_api.include_router(get_routers())

    add_middleware(fast_api)
    return fast_api


app = start_application()
