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
