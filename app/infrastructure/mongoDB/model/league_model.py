from typing import List
from pydantic import Field
from app.infrastructure.mongoDB.model.base_mongo_model import BaseMongoModel
from app.infrastructure.mongoDB.model.race_model import RaceModel
from app.infrastructure.mongoDB.model.runner_league_ranking_model import RunnerLeagueRankingModel
from app.infrastructure.mongoDB.model.runner_model import RunnerModel


class LeagueModel(BaseMongoModel):
    name: str
    races: List[RaceModel] = Field(default_factory=list)
    ranking: List[RunnerLeagueRankingModel] = Field(default_factory=list)
    runners: List[RunnerModel] = Field(default_factory=list)
