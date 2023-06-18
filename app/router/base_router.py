"""_summary_

Returns:
    _type_: _description_
"""
import logging
from typing import Generic, TypeVar
from fastapi import APIRouter, Depends
from app.auth.auth_bearer import JWTBearer
from app.controller.base_controller import BaseController
from app.core.cache import local_cache
from app.router.api_exception import ApiException
from app.router.response_base import IResponseBase


T = TypeVar("T")


class BaseRouter(Generic[T]):
    """_summary_

    Args:
        APIRouter (_type_): _description_
    """
    controller:BaseController

    def __init__(self, key_cache, controller:BaseController, body_type: T):
        self.router = APIRouter()
        self.controller = controller
        self.key_cache = key_cache
        self.body_type = body_type
        self.load_router()
        self.logger = logging.getLogger(__name__)

    def load_router(self):
        """_summary_
        """
        def add(item:T):
            """_summary_

            Args:
                x (T): _description_
            """
            return self.__add__(item)

        def update_by_id(id: str, new_item: T):
            """_summary_

            Args:
                item_id (str): _description_
                new_item (T): _description_
            """
            return self.__update_by_id__(id, new_item)

        add.__annotations__["item"] = self.body_type
        update_by_id.__annotations__["id"] = str
        update_by_id.__annotations__["new_item"] = self.body_type

        self.router.get('/', response_model=IResponseBase)(self.__get_all__)
        self.router.post('/', dependencies=[Depends(JWTBearer())])(add)
        self.router.get('/{id}')(self.__get_by_id__)
        self.router.put('/', dependencies=[Depends(JWTBearer())])(update_by_id)
        self.router.delete('/{id}', dependencies=[Depends(JWTBearer())])(self.__delete_by_id__)

    def __get_all__(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        try:
            key = self.key_cache + '__get_all__'
            data = local_cache.get(key)

            if not data:
                data = self.controller.get_all()
                local_cache.add(key, data)
            return IResponseBase(items=data)
        except Exception as exception_error: # pylint: disable=broad-except
            self.logger.error("Error retrieving all items: %s", exception_error)
            raise ApiException(500, "Error retrieving all items") from None

    def __add__(self, new_item:Generic[T]):
        """_summary_

        Args:
            runners (LeagueModel): _description_

        Returns:
            _type_: _description_
        """
        print(type(new_item))

        result = self.controller.add(new_item)
        if not result.inserted_id:
            return {'message': 'El item no se ha añadido correctamente.'}

        key = self.key_cache + '__add__'
        local_cache.delete(key)

        return {'message': 'El item se ha añadido correctamente.'}

    def __get_by_id__(self, item_id: str):
        """_summary_

        Args:
            runners_id (str): _description_

        Returns:
            _type_: _description_
        """
        key = self.key_cache + "__add__%s",str(item_id)
        data = local_cache.get(key)

        if not data:
            data = self.controller.get_by_id(item_id)
            local_cache.add(key, data)

        return data

    def __update_by_id__(self, id: str, new_item: Generic[T]):
        """_summary_

        Args:
            id (str): _description_
            items (LeagueModel): _description_

        Returns:
            _type_: _description_
        """
        result = self.controller.update_by_id(id, new_item)
        return result

    def __delete_by_id__(self, item_id: str):
        """_summary_

        Args:
            item_id (str): _description_

        Returns:
            _type_: _description_
        """
        result = self.controller.delete_by_id(item_id)

        key = self.key_cache + '__delete_by_id__'
        local_cache.delete(key)

        return result
