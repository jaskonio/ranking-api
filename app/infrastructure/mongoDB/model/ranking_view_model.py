"""_summary_
"""
from pydantic import BaseModel


class RankingViewModelBase(BaseModel):
    """_summary_

    Args:
        BaseMongoModel (_type_): _description_
    """
    position: int = 0
    photo: str = ''
    points: float = 0
    name: str = ''
    pos_last_race: int = 0
    top_five: int = 0
    participations: int = 0
    best_position: str = ''
    last_position_race: int = 0
    best_avegare_peace: str = ''
    best_position_real: int = 0
