from app.domain.model.race_info_model import RaceModel
from app.infrastructure.mongoDB.model.race_info_entity import RaceInfoEntity
from app.infrastructure.mongoDB.repository.mongo_db_repository import MongoDBRepository
from app.infrastructure.mongoDB.repository.race_data_repository import RaceDataRepository


class RaceInfoRepository(MongoDBRepository):
    def __init__(self, race_data_repository:RaceDataRepository):
        super().__init__('race_info', RaceInfoEntity, RaceModel)
        self.__race_data_repository = race_data_repository