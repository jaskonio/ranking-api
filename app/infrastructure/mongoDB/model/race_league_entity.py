from typing import List
from app.infrastructure.mongoDB.model.base_mongo_entity import BaseMongoEntity
from app.infrastructure.mongoDB.model.participant_race_entity_property import ParticipantRaceEntityProperty
from app.infrastructure.mongoDB.model.runner_race_data_entity_property import RunnerRaceDataEntityProperty


class RaceLeagueEntity(BaseMongoEntity):
    data: List[RunnerRaceDataEntityProperty] = []
    race_row_id: str = ''
    race_participant: list[ParticipantRaceEntityProperty] = []
