from typing import List
from app.aplication.race_info_service import RaceInfoService
from app.domain.model.race_info_model import RaceInfoRawModel
from app.domain.model.race_league_model import RaceLeagueModel, RaceLeagueRawModel
from app.domain.model.runner_race_data_model import RunnerRaceDataModel
from app.infrastructure.mongoDB.model.race_info_entity import RaceInfoEntity
from app.infrastructure.mongoDB.model.race_league_entity import RaceLeagueEntity
from app.infrastructure.mongoDB.model.runner_race_data_entity import RunnerRaceDataEntity
from app.infrastructure.repository.repository_utils import load_repository_from_config

class RaceLeagueService():

    def __init__(self):
        db = load_repository_from_config()
        self.__race_league_repository = db.get_repository('race_league', RaceLeagueEntity)
        self.__race_info_repository = db.get_repository('race_info', RaceInfoEntity)
        self.__runner_race_data_repository = db.get_repository('runner_race_data', RunnerRaceDataEntity)
        self.__race_info_service = RaceInfoService()

    def get_all(self) -> List[RaceLeagueModel]:
        race_entities:List[RaceLeagueEntity] = self.__race_league_repository.get_all()

        return [race_entity.to_domain_model(RaceLeagueModel) for race_entity in race_entities]

    def get_by_id(self, race_id:str) -> RaceLeagueModel:
        race_entity:RaceLeagueEntity = self.__race_league_repository.get_by_id(race_id)

        return race_entity.to_domain_model(RaceLeagueModel)

    def add(self, new_race: RaceLeagueModel) -> RaceLeagueModel:
        race_id = self.__race_league_repository.add(RaceLeagueEntity().create_by_domain_model(new_race))

        race_entity:RaceLeagueEntity = self.__race_league_repository.get_by_id(race_id)

        return race_entity.to_domain_model(RaceLeagueModel)

    def update_by_id(self, race_id:str, new_race:RaceLeagueModel) -> RaceLeagueModel:
        status = self.__race_league_repository.update_by_id(race_id, RaceLeagueEntity().create_by_domain_model(new_race))

        if status:
            race_entity:RaceLeagueEntity = self.__race_league_repository.get_by_id(race_id)
            return race_entity.to_domain_model(RaceLeagueModel)
        else:
            return None

    def delete_by_id(self, race_id) -> bool:
        status = self.__race_league_repository.delete_by_id(race_id)

        if status:
            return status

        return None

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
