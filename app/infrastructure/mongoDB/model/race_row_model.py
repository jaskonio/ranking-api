from typing import List
from app.infrastructure.mongoDB.model.base_mongo_model import BaseMongoModel
from app.infrastructure.mongoDB.model.runner_race_row_model import RunnerRaceRowModel


class RaceRowModel(BaseMongoModel):
    name: str
    url: str = ''
    platform: str = ''
    processed: bool = False
    photo: str = ''
    data: List[RunnerRaceRowModel] = []
