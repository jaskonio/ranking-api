from typing import List, Optional
from app.domain.model.season_model import SeasonRawModel
from app.infrastructure.mongoDB.model.season_entity import SeasonEntity
from app.infrastructure.mongoDB.repository.league_repository import LeagueRepository
from app.infrastructure.mongoDB.repository.mongo_db_repository import MongoDBRepository


class SeassonRepository(MongoDBRepository):
    def __init__(self):
        super().__init__('seasson')
        self.__league_repository = LeagueRepository()

    def get_all_raw(self) -> List[SeasonRawModel]:
        season_entities: List[SeasonEntity] = self.get_all()
        league_models = self.__league_repository.get_all_raw()

        season_models:List[SeasonRawModel] = []

        for season_entity in season_entities:
            season_model:SeasonRawModel = season_entity.to_domain_model(SeasonRawModel)

            for league_model in league_models:
                if league_model.id in season_entity.league_ids:
                    season_model.leagues.append(league_model)

            season_models.append(season_model)

        return season_models

    def get_raw_by_id(self, entity_id:str) -> Optional[SeasonRawModel]:
        season_entity: SeasonEntity = self.get_by_id(entity_id)
        league_models = self.__league_repository.get_all_raw()

        season_model:SeasonRawModel = season_entity.to_domain_model(SeasonRawModel)

        for league_model in league_models:
            if league_model.id in season_entity.league_ids:
                season_model.leagues.append(league_model)

        return season_model
