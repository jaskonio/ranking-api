from typing import List
from app.infrastructure.mongoDB.model.entity_base_mongo_model import EntityBaseMongoModel
from app.infrastructure.mongoDB.model.runner_race_data_model import RunnerRaceDataModel


class RaceDataModel(EntityBaseMongoModel):
    data: List[RunnerRaceDataModel] = []
