"""
TODO
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .infrastructure.mongoDB.mongoDB_utils import close_mongo_connection, connect_to_mongo
from .core.config import Settings

connect_to_mongo(Settings.MONGODB_URI, Settings.MONGODB_DATABASE)

from app.router.base import get_routers

def add_middleware(fast_api: FastAPI):
    """
    TODO
    """
    origins = ["*"]

    fast_api.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def start_application():
    """
    TODO
    """
    fast_api = FastAPI(title=Settings.PROJECT_NAME, version=Settings.PROJECT_VERSION)
    logging.info("connect_to_mongo")

    logging.info("include_router")
    fast_api.include_router(get_routers())

    add_middleware(fast_api)
    return fast_api

app = start_application()

app.add_event_handler("shutdown", close_mongo_connection)
