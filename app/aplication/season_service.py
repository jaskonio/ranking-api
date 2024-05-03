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


