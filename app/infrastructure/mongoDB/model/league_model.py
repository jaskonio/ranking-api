import logging
from typing import List
from app.infrastructure.mongoDB.model.BaseMongoModel import BaseMongoModel
from pydantic import Field


logger = logging.getLogger(__name__)

class LeagueModel(BaseMongoModel):
    """_summary_

    Args:
        BaseMongoModel (_type_): _description_

    Returns:
        _type_: _description_
    """
    name: str
    races: List[RaceModel] = Field(default_factory=list)
    final_ranking: List[RankingViewModelBase] = Field(default_factory=list)
    runnerParticipants: List[RunnerParticipantModel] = Field(default_factory=list)
