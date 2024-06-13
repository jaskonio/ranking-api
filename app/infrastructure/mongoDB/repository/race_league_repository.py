from typing import List, Optional
from app.domain.model.race_info_model import RaceInfoRawModel
from app.domain.repository.igeneric_repository import IGenericRepository
from app.infrastructure.mongoDB.model.race_league_entity import RaceLeagueEntity
from app.infrastructure.mongoDB.repository.mongo_db_repository import MongoDBRepository


class RaceLeagueRepository(MongoDBRepository):
    def __init__(self, runner_race_data_repository:IGenericRepository, race_info_repository:IGenericRepository):
        super().__init__('race_league', RaceLeagueEntity, RaceLeagueModel)
        self.__runner_race_data_repository = runner_race_data_repository
        self.__race_info_repository = race_info_repository

    def get_all_raw(self) -> List[RaceLeagueRawModel]:
        all_race_league_models:List[RaceLeagueModel] = self.get_all()

        if len(all_race_league_models) == 0:
            return all_race_league_models

        all_raw_race_info_models:List[RaceInfoRawModel] = self.__race_info_repository.get_all_raw()
        all_runner_race_data_models:List[RunnerRaceDataModel] = self.__runner_race_data_repository.get_all()

        all_raw_race_league_models: List[RaceLeagueRawModel] = []

        for race_league_model in all_race_league_models:
            raw_race_league_model: RaceLeagueRawModel = RaceLeagueRawModel()
            raw_race_league_model.id = race_league_model.id
            raw_race_league_model.order = race_league_model.order

            for raw_race_info_model in all_raw_race_info_models:
                if race_league_model.race_row_id == raw_race_info_model.id:
                    raw_race_league_model.race_info = raw_race_info_model

            for runners_id in race_league_model.ranking:
                for runner_race_data_model in all_runner_race_data_models:
                    if runners_id == runner_race_data_model.id:
                        raw_race_league_model.runners.append(runner_race_data_model)

            all_raw_race_league_models.append(raw_race_league_model)

        return all_raw_race_league_models

    def get_raw_by_id(self, model_id:str) -> Optional[RaceLeagueRawModel]:
        race_league_model:RaceLeagueModel = self.get_by_id(model_id)

        if race_league_model is None:
            return None

        raw_race_info_model:RaceInfoRawModel = self.__race_info_repository.get_raw_by_id(race_league_model.race_row_id)
        all_runner_race_data_models:List[RunnerRaceDataModel] = self.__runner_race_data_repository.get_all()

        raw_race_league_model: RaceLeagueRawModel = RaceLeagueRawModel()
        raw_race_league_model.id = race_league_model.id
        raw_race_league_model.order = race_league_model.order
        raw_race_league_model.race_info = raw_race_info_model

        for runners_id in race_league_model.ranking:
            for runner_race_data_model in all_runner_race_data_models:
                if runners_id == runner_race_data_model.id:
                    raw_race_league_model.runners.append(runner_race_data_model)

        return raw_race_league_model
