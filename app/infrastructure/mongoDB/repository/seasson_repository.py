from typing import List, Optional
from app.domain.model.season_model import SeasonModel
from app.infrastructure.mongoDB.model.season_entity import SeasonEntity
from app.infrastructure.mongoDB.repository.league_repository import LeagueRepository
from app.infrastructure.mongoDB.repository.mongo_db_repository import MongoDBRepository


class SeassonRepository(MongoDBRepository):
    def __init__(self, league_repository:LeagueRepository):
        super().__init__('seasson', SeasonEntity, SeasonModel)
        self.__league_repository = league_repository

    def get_all(self) -> List[SeasonModel]:
        result_dict = list(self.collection.find({}))

        if len(result_dict) == 0:
            return []

        season_entities:List[SeasonEntity] = [SeasonEntity(**entity) for entity in result_dict]

        all_league_models = self.__league_repository.get_all()

        all_season_model:List[SeasonModel] = []

        for season_entity in season_entities:
            season_model = SeasonModel()
            season_model.id = season_entity.id
            season_model.name = season_entity.name
            season_model.order = season_entity.order

            for league_model in all_league_models:
                if league_model.id in season_entity.league_ids:
                    season_model.leagues.append(league_model)

            all_season_model.append(season_model)

        return all_season_model

    def get_by_id(self, model_id:str) -> Optional[SeasonModel]:
        season_model: SeasonModel = self.get_by_id(model_id)
        all_raw_league_models = self.__league_repository.get_all_raw()

        raw_season_model:SeasonModel = SeasonModel()
        raw_season_model.id = season_model.id
        raw_season_model.name = season_model.name

        for raw_league_model in all_raw_league_models:
            if raw_league_model.id in season_model.league_ids:
                raw_season_model.leagues.append(raw_league_model)

        return raw_season_model
