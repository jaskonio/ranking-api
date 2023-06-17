"""_summary_
"""
from app.model.BaseMongoModel import BaseMongoModel


class PersonModel(BaseMongoModel):
    """_summary_

    Args:
        BaseMongoModel (_type_): _description_
    """
    first_name: str
    last_name: str
    photo: str = ''
