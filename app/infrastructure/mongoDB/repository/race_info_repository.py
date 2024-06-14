from app.domain.model.race_info_model import RaceModel
from app.infrastructure.mongoDB.model.race_info_entity import RaceInfoEntity
from app.infrastructure.mongoDB.repository.mongo_db_repository import MongoDBRepository


class RaceInfoRepository(MongoDBRepository):
    def __init__(self):
        super().__init__('race_info', RaceInfoEntity, RaceModel)