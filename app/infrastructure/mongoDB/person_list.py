"""_summary_

Returns:
    _type_: _description_
"""
from app.infrastructure.mongoDB.base_list import BaseList
from app.model.person_model import PersonModel


class PersonList(BaseList):
    """_summary_
    """
    def __init__(self):
        collection_name = "PersonList"
        super().__init__(collection_name, PersonModel)

    def get_all(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        results = self.collection.find()

        leagues = []

        for result in results:
            person_model = PersonModel.from_mongo(result)
            person_model.build_properties()
            leagues.append(person_model)

        return leagues