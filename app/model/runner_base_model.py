"""_summary_
"""

from pydantic import BaseModel


class RunnerBaseModel(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    dorsal: int
    name: str = ''
    club: str = 'Redolat Team'
    nationality: str = ''
    gender: str = ''
    category: str = ''
