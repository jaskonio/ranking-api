import logging
from typing import List
from app.aplication.race_league_service import RaceLeagueService
from app.domain.model.race_league_model import RaceLeagueModel
from app.infrastructure.rest_api.model.race_league_model import RaceLeagueRawResponse, RaceLeagueResponse


class RaceLeagueController():
    def __init__(self):
        self.__race_league_service = RaceLeagueService()
        self.logger = logging.getLogger(__name__)

    def get_all(self) -> List[RaceLeagueResponse]:
        try:
            results = self.__race_league_service.get_all()
            results = [RaceLeagueResponse().create_by_domain_model(result) for result in results]
            return results
        except Exception as exception_error:
            self.logger.error("Error retrieving all items: %s", exception_error)
            raise TypeError('An error occurred while retrieving all items.') from None

    def get_by_id(self, race_id) -> RaceLeagueResponse:
        try:
            race = self.__race_league_service.get_by_id(race_id)

            if race:
                return RaceLeagueResponse().create_by_domain_model(race)

            return {}
        except Exception as exception_error:
            self.logger.error("Error retrieving item: %s", exception_error)
            raise TypeError('An error occurred while retrieving item.') from None

    def add(self, race:RaceLeagueResponse) -> RaceLeagueResponse:
        try:
            race = self.__race_league_service.add(race.to_domain_model(RaceLeagueModel))

            if race:
                return RaceLeagueResponse().create_by_domain_model(race)

            return {}
        except Exception as exception_error:
            self.logger.error("Error saving: %s", exception_error)
            raise TypeError('An error occurred while saving.') from None


    def update_by_id(self, race_id:str, new_race) -> RaceLeagueResponse:
        try:
            race = self.__race_league_service.update_by_id(race_id, new_race)

            if race:
                return RaceLeagueResponse().create_by_domain_model(race)

            return {}
        except Exception as exception_error:
            self.logger.error("Error updating: %s", exception_error)
            raise TypeError('An error occurred while updating.') from None

    def delete_by_id(self, race_id) -> bool:
        try:
            status = self.__race_league_service.delete_by_id(race_id)

            if status:
                return status

            return {}
        except Exception as exception_error:
            self.logger.error("Error deleting: %s", exception_error)
            raise TypeError('An error occurred while deleting.') from None

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
