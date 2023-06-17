"""_summary_

Returns:
    _type_: _description_
"""
from bson import ObjectId
from app.infrastructure.mongoDB.interface_list import BaseInterfaceList
from app.model.BaseMongoModel import BaseMongoModel


class BaseList(BaseInterfaceList):
    """_summary_
    """
    def get_all(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        results = self.collection.find()

        leagues = []

        for result in results:
            leagues.append(self.object.from_mongo(result))

        return leagues

    def add(self, item: BaseMongoModel):
        """_summary_

        Args:
            item (BaseMongoModel): _description_

        Returns:
            _type_: _description_
        """
        item = self.object(item)
        result = self.collection.insert_one(item.mongo())

        return result

    def get_by_id(self, str_id):
        """_summary_

        Args:
            str_id (_type_): _description_

        Returns:
            _type_: _description_
        """
        race = self.collection.find_one({'_id': ObjectId(str_id)})

        return BaseMongoModel.from_mongo(race)

    def update_by_id(self, old_item_id, new_item:BaseMongoModel):
        """_summary_

        Args:
            old_item_id (_type_): _description_
            new_item (BaseMongoModel): _description_

        Returns:
            _type_: _description_
        """
        item_dict = new_item.mongo()
        return self.collection.update_one({'_id': ObjectId(old_item_id)}, {'$set': item_dict})

    def delete_by_id(self, item_id):
        """_summary_

        Args:
            item_id (_type_): _description_

        Returns:
            _type_: _description_
        """
        return self.collection.delete_one({"_id": ObjectId(item_id)})
