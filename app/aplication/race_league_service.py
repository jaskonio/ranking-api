from typing import List
from app.aplication.base_service import BaseService
from app.aplication.race_info_service import RaceInfoService
from app.domain.model.race_info_model import RaceInfoRawModel
from app.domain.model.race_league_model import RaceLeagueModel, RaceLeagueRawModel
from app.domain.model.runner_race_data_model import RunnerRaceDataModel
from app.infrastructure.mongoDB.model.race_league_entity import RaceLeagueEntity
from app.infrastructure.mongoDB.model.runner_race_data_entity import RunnerRaceDataEntity


class RaceLeagueService(BaseService):
    def __init__(self, race_league_repository, runner_race_data_repository, race_info_service:RaceInfoService):
        super().__init__(race_league_repository, RaceLeagueModel, RaceLeagueEntity)
        self.__race_league_repository = race_league_repository
        self.__runner_race_data_repository = runner_race_data_repository
        self.__race_info_service = race_info_service

    def get_all_raw(self) -> List[RaceLeagueRawModel]:
        race_league_entities:List[RaceLeagueEntity] = self.__race_league_repository.get_all()
        runner_race_data_entities:List[RunnerRaceDataEntity] = self.__runner_race_data_repository.get_all()

        race_league_models: List[RaceLeagueRawModel] = []

        for race_league_entity in race_league_entities:
            race_league_model: RaceLeagueRawModel = race_league_entity.to_domain_model(RaceLeagueRawModel)

            race_info_raw_model:RaceInfoRawModel = self.__race_info_service.get_raw_by_id(race_league_entity.race_row_id)
            race_league_model.race_info = race_info_raw_model

            for runners_id in race_league_entity.runners_ids:
                for runner_race_data_entity in runner_race_data_entities:
                    if runners_id == runner_race_data_entity.id:
                        race_league_model.runners.append(runner_race_data_entity.to_domain_model(RunnerRaceDataModel))

            race_league_models.append(race_league_model)

        return race_league_models

    def get_raw_by_id(self, race_id:str) -> RaceLeagueRawModel:
        race_league_entity:RaceLeagueEntity = self.__race_league_repository.get_by_id(race_id)

        race_info_raw_model:RaceInfoRawModel = self.__race_info_service.get_raw_by_id(race_league_entity.race_row_id)

        race_league_model:RaceLeagueRawModel = race_league_entity.to_domain_model(RaceLeagueRawModel)

        race_league_model.runners = race_info_raw_model.race_data.runners

        return race_league_model
