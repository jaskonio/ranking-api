import logging
from typing import List
from app.aplication.league_service import LeagueService
from app.domain.model.league_model import LeagueModel, LeagueRAWModel
from app.infrastructure.mongoDB.model.league_entity import LeagueEntity
from app.infrastructure.rest_api.model.league_model import LeagueRawResponse, LeagueRequest, LeagueResponse


class LeagueController():
    def __init__(self, league_service:LeagueService):
        self.logger = logging.getLogger(__name__)
        self.__league_service = league_service

    def get_all(self) -> List[LeagueResponse]:
        try:
            models: List[LeagueEntity] = self.__league_service.get_all()
            return [LeagueResponse().create_by_domain_model(model) for model in models]
        except Exception as exception_error:
            self.logger.error("Error retrieving all items: %s", exception_error)
            raise TypeError('An error occurred while retrieving all items.') from None

    def get_by_id(self, league_id:str) -> LeagueResponse:
        try:
            league_model = self.__league_service.get_by_id(league_id)

            if league_model:
                return LeagueResponse().create_by_domain_model(league_model)

            return {}
        except Exception as exception_error:
            self.logger.error("Error retrieving item: %s", exception_error)
            raise TypeError('An error occurred while retrieving item.') from None

    def add(self, league: LeagueRequest) -> LeagueResponse:
        try:
            league_model:LeagueModel = self.__league_service.add(league.to_domain_model(LeagueModel))

            if league_model:
                return LeagueResponse().create_by_domain_model(league_model)

            return {}
        except Exception as exception_error:
            self.logger.error("Error saving: %s", exception_error)
            raise TypeError('An error occurred while saving.') from None

    def update_by_id(self, league_id:str, new_league: LeagueRequest) -> LeagueResponse:
        try:
            league_model = self.__league_service.update_by_id(league_id, new_league.to_domain_model(LeagueModel))

            if league_model:
                return LeagueResponse().create_by_domain_model(league_model)

            return {}
        except Exception as exception_error:
            self.logger.error("Error updating: %s", exception_error)
            raise TypeError('An error occurred while updating.') from None

    def delete_by_id(self, league_id) -> bool:
        try:
            status = self.__league_service.delete_by_id(league_id)

            if status:
                return status

            return {}
        except Exception as exception_error:
            self.logger.error("Error deleting: %s", exception_error)
            raise TypeError('An error occurred while deleting.') from None

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
