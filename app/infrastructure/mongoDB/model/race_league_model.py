from typing import List
from app.infrastructure.mongoDB.model.base_mongo_model import BaseMongoModel
from app.infrastructure.mongoDB.model.participant_race_model import ParticipantRaceModel
from app.infrastructure.mongoDB.model.runner_race_row_model import RunnerRaceRowModel


class RaceLeagueModel(BaseMongoModel):
    name: str
    url: str = ''
    race_row_id: str = ''
    race_participant: list[ParticipantRaceModel] = []
    data: List[RunnerRaceRowModel] = []
