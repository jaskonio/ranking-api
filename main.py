import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Infrastructure.MongoDB.mongoDB_utils import close_mongo_connection, connect_to_mongo
from apis.base import api_router
from core.config import Settings

def add_middleware(app: FastAPI):
    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def include_router(app:FastAPI):
    app.include_router(api_router)

def start_application():
    app = FastAPI(title=Settings.PROJECT_NAME, version=Settings.PROJECT_VERSION)
    connect_to_mongo(Settings.MONGODB_URI, Settings.MONGODB_DATABASE)
    include_router(app)
    add_middleware(app)    
    return app


app = start_application()

app.add_event_handler("shutdown", close_mongo_connection)

