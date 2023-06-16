"""_summary_

Returns:
    _type_: _description_
"""
from abc import ABC, abstractmethod
from pymongo import collection
from app.model.BaseMongoModel import BaseMongoModel
from app.infrastructure.mongoDB.MongoDBSession import get_database


class BaseInterfaceList(ABC):
    """_summary_
    """
    def __init__(self, collection_name, obj:BaseMongoModel):
        name = collection_name
        self.database = get_database()
        self.collection:collection.Collection = self.database.get_collection(name)
        self.object = obj

    @abstractmethod
    def get_all(self):
        """_summary_
        """
        return

    @abstractmethod
    def add(self, item: BaseMongoModel):
        """_summary_

        Args:
            item (BaseMongoModel): _description_

        Returns:
            _type_: _description_
        """
        return

    @abstractmethod
    def get_by_id(self, str_id):
        """_summary_

        Args:
            str_id (_type_): _description_

        Returns:
            _type_: _description_
        """
        return

    @abstractmethod
    def update_by_id(self, old_item_id, new_item:BaseMongoModel):
        """_summary_

        Args:
            old_item_id (_type_): _description_
            new_item (BaseMongoModel): _description_

        Returns:
            _type_: _description_
        """
        return

    @abstractmethod
    def delete_by_id(self, item_id):
        """_summary_

        Args:
            item_id (_type_): _description_

        Returns:
            _type_: _description_
        """
        return
