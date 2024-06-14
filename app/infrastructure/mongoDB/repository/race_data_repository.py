from typing import List, Optional
from app.domain.model.race_data_model import RaceDataModel, RaceDataModel, RunnerRaceDataModel
from app.infrastructure.mongoDB.model.race_data_entity import RaceDataEntity
from app.infrastructure.mongoDB.repository.mongo_db_repository import MongoDBRepository


class RaceDataRepository(MongoDBRepository):
    def __init__(self):
        super().__init__('race_data', RaceDataEntity, RaceDataModel)