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
