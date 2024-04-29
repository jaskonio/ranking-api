from typing import List
from app.aplication.base_service import BaseService
from app.aplication.league_service import LeagueService
from app.domain.model.season_model import SeasonModel, SeasonRawModel
from app.domain.repository.igeneric_repository import IGenericRepository
from app.infrastructure.mongoDB.model.season_entity import SeasonEntity


class SeasonService(BaseService):

    def __init__(self, season_repository:IGenericRepository, season_model_domain:SeasonModel, season_entity_type:SeasonEntity, league_service:LeagueService) -> None:
        super().__init__(season_repository, season_model_domain, season_entity_type)
        self.__league_service = league_service

    def get_all_raw(self) -> List[SeasonModel]:
        season_entities: List[SeasonEntity] = self.__repository.get_all()
        league_models = self.__league_service.get_all_raw()

        season_models:List[SeasonModel] = []

        for season_entity in season_entities:
            season_model:SeasonRawModel = season_entity.to_domain_model(SeasonRawModel)

            for league_model in league_models:
                if league_model.id in season_entity.league_ids:
                    season_model.leagues.append(league_model)

            season_models.append(season_model)

        return season_models

    def get_raw_by_id(self, season_id:str) -> SeasonModel:
        season_entity: SeasonEntity = self.__repository.get_by_id(season_id)
        league_models = self.__league_service.get_all_raw()

        season_model:SeasonRawModel = season_entity.to_domain_model(SeasonRawModel)

        for league_model in league_models:
            if league_model.id in season_entity.league_ids:
                season_model.leagues.append(league_model)

        return season_model
