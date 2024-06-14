from typing import List, Optional
from app.domain.model.race_data_model import RaceDataRawModel
from app.domain.model.race_info_model import RaceModel
from app.infrastructure.mongoDB.model.race_info_entity import RaceInfoEntity
from app.infrastructure.mongoDB.repository.mongo_db_repository import MongoDBRepository
from app.infrastructure.mongoDB.repository.race_data_repository import RaceDataRepository


class RaceInfoRepository(MongoDBRepository):
    def __init__(self, race_data_repository:RaceDataRepository):
        super().__init__('race_info', RaceInfoEntity, RaceModel)
        self.__race_data_repository = race_data_repository

    def get_all_raw(self) -> List[RaceModel]:
        all_race_info_models:List[RaceModel] = self.get_all()
        all_raw_race_data_model:List[RaceDataRawModel] = self.__race_data_repository.get_all_raw()

        all_race_info_model:List[RaceModel] = []

        for race_info_model in all_race_info_models:
            raw_race_info_model:RaceModel = RaceModel()
            raw_race_info_model.id = race_info_model.id
            raw_race_info_model.name = race_info_model.name
            raw_race_info_model.url = race_info_model.url
            raw_race_info_model.platform = race_info_model.platform
            raw_race_info_model.processed = race_info_model.processed

            for raw_race_data_model in all_raw_race_data_model:
                if race_info_model.id == raw_race_data_model.id:
                    raw_race_info_model.race_data = raw_race_data_model

            all_race_info_model.append(raw_race_info_model)

        return all_race_info_model

    def get_raw_by_id(self, model_id:str) -> Optional[RaceModel]:
        race_info_model:RaceModel = self.get_by_id(model_id)
        raw_race_data_model:RaceDataRawModel = self.__race_data_repository.get_raw_by_id(race_info_model.race_data_id)

        raw_race_info_model:RaceModel = RaceModel()
        raw_race_info_model.id = race_info_model.id
        raw_race_info_model.name = race_info_model.name
        raw_race_info_model.url = race_info_model.url
        raw_race_info_model.platform = race_info_model.platform
        raw_race_info_model.processed = race_info_model.processed
        raw_race_info_model.race_data = raw_race_data_model

        return raw_race_info_model
