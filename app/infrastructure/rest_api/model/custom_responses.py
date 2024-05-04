from typing import Any
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class BaseSuccessJsonResponse(BaseModel):
    status_code: int = 200
    status:str = "success"
    message:str = 'Success'
    data: Any

class FailJsonResponse(BaseModel):
    status:str = "fail"
    message:str = 'Invalid Request'
    data: Any
    status_code: int = 400

class ErrorJsonResponse(BaseModel):
    status:str = "error"
    message:str = 'Internal Server Error'
    status_code: int = 500

class CustomStaticJSONResponse:
    @staticmethod
    def success(data=None, message="Success", status_code=200):
        data_dict = None
        if isinstance(data, BaseModel):
            data_dict = data.dict(exclude_none=True)
        elif isinstance(data, list):
            data_dict = [v.dict(exclude_none=True) for v in data]

        response_body = {
            "status": "success",
            "message": message,
            "data": data_dict
        }
        return JSONResponse(content=response_body, status_code=status_code)

    @staticmethod
    def error(message="Internal Server Error", status_code=500):
        response_body = {
            "status": "error",
            "message": message
        }
        return JSONResponse(content=response_body, status_code=status_code)

    @staticmethod
    def invalid_request(errors=None, message="Invalid Request", status_code=400):
        response_body = {
            "status": "fail",
            "message": message,
            "errors": errors
        }
        return JSONResponse(content=response_body, status_code=status_code)
