"""_summary_
"""
from app.model.BaseMongoModel import BaseMongoModel

class RunnerBaseModel(BaseMongoModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    name: str
    last_name: str = ''
    dorsal: int = 0
    club: str = 'Redolat Team'
    nationality: str = ''
    gender: str = ''
    category: str = ''
    photo: str = ''
    person_id: str = ''
