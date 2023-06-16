"""_summary_
"""
from pydantic import Field
from app.model.BaseMongoModel import BaseMongoModel
from app.model.OID import OID


class PersonModel(BaseMongoModel):
    """_summary_

    Args:
        BaseMongoModel (_type_): _description_
    """
    id: OID = Field(default_factory=OID)
    first_name: str
    last_name: str
    photo: str = ''
