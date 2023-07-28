"""_summary_
"""
from pydantic import BaseModel


class RunnerParticipantModel(BaseModel):
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
