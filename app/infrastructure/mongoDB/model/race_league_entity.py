from typing import List
from app.infrastructure.mongoDB.model.base_mongo_entity import BaseMongoEntity
from app.infrastructure.mongoDB.model.runner_race_data_entity_property import RunnerRaceDataEntityProperty


class RaceLeagueEntity(BaseMongoEntity):
    race_row_id: str = ''
    order: int = 0
    ranking: List[RunnerRaceDataEntityProperty] = []
