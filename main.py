import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Infrastructure.MongoDB.mongoDB_utils import close_mongo_connection, connect_to_mongo
from core.config import Settings

connect_to_mongo(Settings.MONGODB_URI, Settings.MONGODB_DATABASE)

from apis.base import get_routers


def add_middleware(app: FastAPI):
    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
   
def start_application():
    app = FastAPI(title=Settings.PROJECT_NAME, version=Settings.PROJECT_VERSION)
    logging.info("connect_to_mongo")
    
    logging.info("include_router")
    app.include_router(get_routers())
        
    add_middleware(app)    
    return app

app = start_application()

app.add_event_handler("shutdown", close_mongo_connection)

