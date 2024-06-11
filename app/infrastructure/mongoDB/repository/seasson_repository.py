from typing import List, Optional
from app.domain.model.season_model import SeasonRawModel, SeasonModel
from app.infrastructure.mongoDB.model.season_entity import SeasonEntity
from app.infrastructure.mongoDB.repository.league_repository import LeagueRepository
from app.infrastructure.mongoDB.repository.mongo_db_repository import MongoDBRepository


class SeassonRepository(MongoDBRepository):
    def __init__(self, league_repository:LeagueRepository):
        super().__init__('seasson', SeasonEntity, SeasonModel)
        self.__league_repository = league_repository

    def get_all_raw(self) -> List[SeasonRawModel]:
        all_season_models: List[SeasonModel] = self.get_all()
        all_raw_league_models = self.__league_repository.get_all_raw()

        all_raw_season_models:List[SeasonRawModel] = []

        for season_model in all_season_models:
            raw_season_model:SeasonRawModel = SeasonRawModel()
            raw_season_model.id = season_model.id
            raw_season_model.name = season_model.name

            for raw_league_model in all_raw_league_models:
                if raw_league_model.id in season_model.league_ids:
                    raw_season_model.leagues.append(raw_league_model)

            all_raw_season_models.append(season_model)

        return all_raw_season_models

    def get_raw_by_id(self, model_id:str) -> Optional[SeasonRawModel]:
        season_model: SeasonModel = self.get_by_id(model_id)
        all_raw_league_models = self.__league_repository.get_all_raw()

        raw_season_model:SeasonRawModel = SeasonRawModel()
        raw_season_model.id = season_model.id
        raw_season_model.name = season_model.name

        for raw_league_model in all_raw_league_models:
            if raw_league_model.id in season_model.league_ids:
                raw_season_model.leagues.append(raw_league_model)

        return raw_season_model
