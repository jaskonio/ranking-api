from typing import List, Optional
from app.domain.model.race_data_model import RaceDataRawModel
from app.domain.model.race_info_model import RaceInfoRawModel
from app.infrastructure.mongoDB.model.race_info_entity import RaceInfoEntity
from app.infrastructure.mongoDB.repository.mongo_db_repository import MongoDBRepository
from app.infrastructure.mongoDB.repository.race_data_repository import RaceDataRepository


class RaceInfoRepository(MongoDBRepository):
    def __init__(self):
        super().__init__('race_info')
        self.__race_data_repository = RaceDataRepository()

    def get_all_raw(self) -> List[RaceInfoRawModel]:
        all_race_info_entities:List[RaceInfoEntity] = self.get_all()
        all_raw_race_data_model:List[RaceDataRawModel] = self.__race_data_repository.get_all_raw()

        all_race_info_model:List[RaceInfoRawModel] = []

        for race_info_entity in all_race_info_entities:
            race_info_model:RaceInfoRawModel = race_info_entity.to_domain_model(RaceInfoRawModel)

            for raw_race_data_model in all_raw_race_data_model:
                if race_info_entity.race_data_id == raw_race_data_model.id:
                    race_info_model.race_data = raw_race_data_model

            all_race_info_model.append(race_info_model)

        return all_race_info_model

    def get_raw_by_id(self, entity_id:str) -> Optional[RaceInfoRawModel]:
        race_info_entity:RaceInfoEntity = self.get_by_id(entity_id)

        if race_info_entity is None:
            return None

        all_raw_race_data_model:List[RaceDataRawModel] = self.__race_data_repository.get_all_raw()

        race_info_model:RaceInfoRawModel = race_info_entity.to_domain_model(RaceInfoRawModel)

        for raw_race_data_model in all_raw_race_data_model:
            if race_info_entity.race_data_id == raw_race_data_model.id:
                race_info_model.race_data = raw_race_data_model

        return race_info_model
