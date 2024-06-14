import logging
from typing import List
from app.domain.model.league_model import LeagueRace
from app.infrastructure.rest_api.controller.base_controller import BaseController
from app.infrastructure.rest_api.model.race_league_model import RaceLeagueRawResponse, RaceLeagueResponse


class RaceLeagueController(BaseController):
    def __init__(self, race_league_repository, race_league_service):
        super().__init__(race_league_repository, RaceLeagueResponse, LeagueRace)
        self.__race_league_service = race_league_service
        self.logger = logging.getLogger(__name__)

    def get_all_raw(self) -> List[RaceLeagueRawResponse]:
        try:
            results = self.__race_league_service.get_all_raw()
            data_response: List[RaceLeagueRawResponse] = [RaceLeagueRawResponse().create_by_domain_model(result) for result in results]

            return data_response
        except Exception as exception_error:
            self.logger.error("Error retrieving all items: %s", exception_error)
            raise TypeError('An error occurred while retrieving all items.') from None

    def get_raw_by_id(self, race_id: str) -> RaceLeagueRawResponse:
        try:
            result:RaceLeagueModel = self.__race_league_service.get_raw_by_id(race_id)
            data_response = RaceLeagueRawResponse().create_by_domain_model(result)

            return data_response
        except Exception as exception_error:
            self.logger.error("Error retrieving all items: %s", exception_error)
            raise TypeError('An error occurred while retrieving all items.') from None
