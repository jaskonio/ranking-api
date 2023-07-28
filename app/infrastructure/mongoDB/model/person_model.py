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
    photo_url: str = ''

    def build_properties(self):
        self.photo_url = '/images/' + str(self.id)
