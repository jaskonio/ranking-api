import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import Settings
from app.infrastructure.rest_api.route.import_routers import get_routers

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

def start_application():
    fast_api = FastAPI(title=Settings.PROJECT_NAME, version=Settings.PROJECT_VERSION)
    logging.info("connect_to_mongo")

    logging.info("include_router")

    fast_api.include_router(get_routers())

    add_middleware(fast_api)
    return fast_api


# def exception_handler_api_exception(request: Request, exception: ApiException):
#     logger.error(exception.args)
#     return JSONResponse(status_code = exception.code_error,
#                         content = {"message": exception.message})

app = start_application()

#app.add_event_handler("startup", close_mongo_connection)
#app.add_event_handler("shutdown", close_mongo_connection)

#app.add_exception_handler(ApiException, handler=exception_handler_api_exception)
