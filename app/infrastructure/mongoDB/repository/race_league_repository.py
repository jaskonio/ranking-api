from typing import List
from app.domain.model.race_info_model import RaceInfoRawModel
from app.domain.model.race_league_model import RaceLeagueRawModel
from app.domain.model.runner_race_data_model import RunnerRaceDataModel
from app.infrastructure.mongoDB.model.race_league_entity import RaceLeagueEntity
from app.infrastructure.mongoDB.model.runner_race_data_entity import RunnerRaceDataEntity
from app.infrastructure.mongoDB.repository.mongo_db_repository import MongoDBRepository
from app.infrastructure.mongoDB.repository.race_info_repository import RaceInfoRepository


class RaceLeagueRepository(MongoDBRepository):
    def __init__(self):
        super().__init__('race_league')
        self.__runner_race_data_repository = MongoDBRepository('runner_race_data')
        self.__race_info_repository = RaceInfoRepository()

    def get_all_raw(self) -> List[RaceLeagueRawModel]:
        race_league_entities:List[RaceLeagueEntity] = self.get_all()
        runner_race_data_entities:List[RunnerRaceDataEntity] = self.__runner_race_data_repository.get_all()

        race_league_models: List[RaceLeagueRawModel] = []

        for race_league_entity in race_league_entities:
            race_league_model: RaceLeagueRawModel = race_league_entity.to_domain_model(RaceLeagueRawModel)

            race_info_raw_model:RaceInfoRawModel = self.__race_info_repository.get_raw_by_id(race_league_entity.race_row_id)
            race_league_model.race_info = race_info_raw_model

            for runners_id in race_league_entity.runners_ids:
                for runner_race_data_entity in runner_race_data_entities:
                    if runners_id == runner_race_data_entity.id:
                        race_league_model.runners.append(runner_race_data_entity.to_domain_model(RunnerRaceDataModel))

            race_league_models.append(race_league_model)

        return race_league_models

    def get_raw_by_id(self, entity_id:str) -> RaceLeagueRawModel:
        race_league_entity:RaceLeagueEntity = self.get_by_id(entity_id)

        race_info_raw_model:RaceInfoRawModel = self.__race_info_repository.get_raw_by_id(race_league_entity.race_row_id)

        race_league_model:RaceLeagueRawModel = race_league_entity.to_domain_model(RaceLeagueRawModel)

        race_league_model.runners = race_info_raw_model.race_data.runners

        return race_league_model
