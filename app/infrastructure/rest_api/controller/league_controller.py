import logging
from typing import List
from app.aplication.league_service import LeagueService
from app.domain.model.league_model import LeagueRAWModel
from app.infrastructure.rest_api.controller.base_controller import BaseController
from app.infrastructure.rest_api.model.league_model import LeagueRawResponse


class LeagueController(BaseController):
    def __init__(self, league_service:LeagueService, api_model, domain_model):
        super().__init__(league_service, api_model, domain_model)
        self.logger = logging.getLogger(__name__)
        self.__league_service = league_service

    def get_all_raw(self) -> List[LeagueRawResponse]:
        try:
            models: List[LeagueRAWModel] = self.__league_service.get_all_raw()
            return [LeagueRawResponse().create_by_domain_model(model) for model in models]
        except Exception as exception_error:
            self.logger.error("Error retrieving all items: %s", exception_error)
            raise TypeError('An error occurred while retrieving all items.') from None

    def get_raw_by_id(self, league_id:str) -> LeagueRawResponse:
        try:
            league_model = self.__league_service.get_raw_by_id(league_id)

            if league_model:
                return LeagueRawResponse().create_by_domain_model(league_model)

            return {}
        except Exception as exception_error:
            self.logger.error("Error retrieving item: %s", exception_error)
            raise TypeError('An error occurred while retrieving item.') from None

    def run_process_by_id(self, league_id:str) -> LeagueRawResponse:
        try:
            league_model = self.__league_service.run_process(league_id)

            if league_model:
                return LeagueRawResponse().create_by_domain_model(league_model)

            return None
        except Exception as exception_error:
            self.logger.error("Error retrieving item: %s", exception_error)
            raise TypeError('An error occurred while retrieving item.') from None
