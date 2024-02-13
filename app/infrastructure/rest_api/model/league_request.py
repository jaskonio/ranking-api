from typing import List
from pydantic import Field
from app.infrastructure.mongoDB.model.base_mongo_model import BaseMongoModel
from app.infrastructure.rest_api.model.person_request import RunnerBaseRequest
from app.infrastructure.rest_api.model.race_request import RaceRequest
from app.infrastructure.rest_api.model.runner_request import RunnerLeagueRankingRequest


class LeagueRequest(BaseMongoModel):
    name: str
    races:List[RaceRequest] = Field(default_factory=list)
    ranking:List[RunnerLeagueRankingRequest] = Field(default_factory=list)
    participants:List[RunnerBaseRequest] = Field(default_factory=list)
