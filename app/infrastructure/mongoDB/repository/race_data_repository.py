from typing import List, Optional
from app.domain.model.race_data_model import RaceDataRawModel, RaceDataModel
from app.domain.model.runner_race_data_model import RunnerRaceDataModel
from app.infrastructure.mongoDB.model.race_data_entity import RaceDataEntity
from app.infrastructure.mongoDB.model.runner_race_data_entity import RunnerRaceDataEntity
from app.infrastructure.mongoDB.repository.mongo_db_repository import MongoDBRepository


class RaceDataRepository(MongoDBRepository):
    def __init__(self):
        super().__init__('race_data', RaceDataEntity, RaceDataModel)
        self.__runner_race_data_repository = MongoDBRepository('runner_race_data', RunnerRaceDataEntity, RunnerRaceDataModel)

    def get_all_raw(self) -> List[RaceDataRawModel]:
        all_race_data_model:List[RaceDataModel] = self.get_all()
        all_runner_race_data_entities:List[RunnerRaceDataEntity] = self.__runner_race_data_repository.get_all()

        all_raw_race_data_model: List[RaceDataRawModel] = []

        for race_data_model in all_race_data_model:
            raw_race_data_model:RaceDataRawModel = RaceDataRawModel(id=race_data_model.id)

            for runner_id in race_data_model.runner_ids:
                for runner_race_data_entity in all_runner_race_data_entities:
                    if runner_id in runner_race_data_entity.id:
                        raw_race_data_model.runners.append(runner_race_data_entity.to_domain_model(RunnerRaceDataModel))

            all_raw_race_data_model.append(raw_race_data_model)

        return all_raw_race_data_model

    def get_raw_by_id(self, model_id: str) -> Optional[RaceDataRawModel]:
        race_data_model:RaceDataModel = self.get_by_id(model_id)
        all_runner_race_data_entities:List[RunnerRaceDataEntity] = self.__runner_race_data_repository.get_all()

        raw_race_data_model:RaceDataRawModel = RaceDataRawModel(id=race_data_model.id)

        for runner_id in race_data_model.runner_ids:
            for runner_race_data_entity in all_runner_race_data_entities:
                if runner_id in runner_race_data_entity.id:
                    raw_race_data_model.runners.append(runner_race_data_entity.to_domain_model(RunnerRaceDataModel))

        return raw_race_data_model
