from typing import List, Optional
from app.domain.model.race_data_model import RaceDataModel, RaceDataModel, RunnerRaceDataModel
from app.infrastructure.mongoDB.model.race_data_entity import RaceDataEntity
from app.infrastructure.mongoDB.repository.mongo_db_repository import MongoDBRepository
from app.infrastructure.mongoDB.repository.runner_race_data_repository import RunnerRaceDataRepository


class RaceDataRepository(MongoDBRepository):
    def __init__(self, runner_race_data_repository:RunnerRaceDataRepository):
        super().__init__('race_data', RaceDataEntity, RaceDataModel)
        self.__runner_race_data_repository = runner_race_data_repository

    def get_all_raw(self) -> List[RaceDataModel]:
        all_race_data_model:List[RaceDataModel] = self.get_all()
        all_runner_race_data_models:List[RunnerRaceDataModel] = self.__runner_race_data_repository.get_all()

        all_raw_race_data_model: List[RaceDataModel] = []

        for race_data_model in all_race_data_model:
            raw_race_data_model:RaceDataModel = RaceDataModel()
            raw_race_data_model.id = race_data_model.id

            for runner in race_data_model.runners:
                for runner_race_data_model in all_runner_race_data_models:
                    if runner.id in runner_race_data_model.id:
                        raw_race_data_model.runners.append(runner_race_data_model)

            all_raw_race_data_model.append(raw_race_data_model)

        return all_raw_race_data_model

    def get_raw_by_id(self, model_id: str) -> Optional[RaceDataModel]:
        race_data_model:RaceDataModel = self.get_by_id(model_id)
        all_runner_race_data_models:List[RunnerRaceDataModel] = self.__runner_race_data_repository.get_all()

        raw_race_data_model:RaceDataModel = RaceDataModel()
        raw_race_data_model.id = race_data_model.id

        for runner_id in race_data_model.runner_ids:
            for runner_race_data_model in all_runner_race_data_models:
                if runner_id in runner_race_data_model.id:
                    raw_race_data_model.runners.append(runner_race_data_model)

        return raw_race_data_model
