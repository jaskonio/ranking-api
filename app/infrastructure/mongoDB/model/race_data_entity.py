from typing import List
from app.infrastructure.mongoDB.model.base_mongo_entity import BaseMongoEntity
from app.infrastructure.mongoDB.model.runner_race_data_entity_property import RunnerRaceDataEntityProperty


class RaceDataModel(BaseMongoEntity):
    data: List[RunnerRaceDataEntityProperty] = []
