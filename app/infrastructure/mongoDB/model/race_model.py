from typing import List
from pydantic import Field
from app.infrastructure.mongoDB.model.base_mongo_model import BaseMongoModel
from app.infrastructure.mongoDB.model.runner_race_detail_model import RunnerRaceDetailModel


class RaceModel(BaseMongoModel):
    name: str
    url: str
    ranking: List[RunnerRaceDetailModel] = Field(default_factory=list)
    order: int = 0
    is_sorted: bool = False
