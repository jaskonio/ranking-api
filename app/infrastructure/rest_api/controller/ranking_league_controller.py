import logging
from typing import List
from app.aplication.ranking_league_service import RankingLeagueService
from app.domain.model.ranking_league_model import RankingLeagueModel
from app.infrastructure.rest_api.model.ranking_league_model import RankingLeagueRequest, RankingLeagueResponse

class RankingLeagueController():
    def __init__(self):
        self.__participant_league_service = RankingLeagueService()
        self.logger = logging.getLogger(__name__)

    def get_all(self) -> List[RankingLeagueResponse]:
        try:
            models: List[RankingLeagueModel] = self.__participant_league_service.get_all()
            return [RankingLeagueResponse().create_by_domain_model(model) for model in models]
        except Exception as exception_error:
            self.logger.error("Error retrieving all items: %s", exception_error)
            raise TypeError('An error occurred while retrieving all items.') from None

    def get_by_id(self, person_id:str) -> RankingLeagueResponse:
        try:
            model:RankingLeagueModel = self.__participant_league_service.get_by_id(person_id)

            if model:
                return RankingLeagueResponse().create_by_domain_model(model)

            return {}
        except Exception as exception_error:
            self.logger.error("Error retrieving item: %s", exception_error)
            raise TypeError('An error occurred while retrieving item.') from None

    def add(self, new_person: RankingLeagueRequest) -> RankingLeagueResponse:
        try:
            model:RankingLeagueModel = self.__participant_league_service.add(new_person.to_domain_model(RankingLeagueModel))

            if model:
                return RankingLeagueResponse().create_by_domain_model(model)

            return {}
        except Exception as exception_error:
            self.logger.error("Error saving: %s", exception_error)
            raise TypeError('An error occurred while saving.') from None

    def update_by_id(self, person_id:str, new_person: RankingLeagueRequest) -> RankingLeagueResponse:
        try:
            model:RankingLeagueModel = self.__participant_league_service.update_by_id(person_id, new_person.to_domain_model(RankingLeagueModel))

            if model:
                return RankingLeagueResponse().create_by_domain_model(model)

            return {}
        except Exception as exception_error:
            self.logger.error("Error updating: %s", exception_error)
            raise TypeError('An error occurred while updating.') from None

    def delete_by_id(self, person_id:str) -> bool:
        try:
            status = self.__participant_league_service.delete_by_id(person_id)

            if status:
                return status

            return {}
        except Exception as exception_error:
            self.logger.error("Error deleting: %s", exception_error)
            raise TypeError('An error occurred while deleting.') from None
