import logging
from typing import List

from app.aplication.particpant_league_service import ParticipantLeagueService
from app.domain.model.participant_league_model import ParticipantLeagueModel
from app.infrastructure.rest_api.model.participant_league_model import ParticipantLeagueRequest, ParticipantLeagueResponse


class ParticipantLeagueController():
    def __init__(self):
        self.__participant_league_service = ParticipantLeagueService()
        self.logger = logging.getLogger(__name__)

    def get_all(self) -> List[ParticipantLeagueResponse]:
        try:
            models: List[ParticipantLeagueModel] = self.__participant_league_service.get_all()
            return [ParticipantLeagueResponse().create_by_domain_model(model) for model in models]
        except Exception as exception_error:
            self.logger.error("Error retrieving all items: %s", exception_error)
            raise TypeError('An error occurred while retrieving all items.') from None

    def get_by_id(self, person_id:str) -> ParticipantLeagueResponse:
        try:
            model:ParticipantLeagueModel = self.__participant_league_service.get_by_id(person_id)

            if model:
                return ParticipantLeagueResponse().create_by_domain_model(model)

            return {}
        except Exception as exception_error:
            self.logger.error("Error retrieving item: %s", exception_error)
            raise TypeError('An error occurred while retrieving item.') from None

    def add(self, new_person: ParticipantLeagueRequest) -> ParticipantLeagueResponse:
        try:
            model:ParticipantLeagueModel = self.__participant_league_service.add(new_person.to_domain_model(ParticipantLeagueModel))

            if model:
                return ParticipantLeagueResponse().create_by_domain_model(model)

            return {}
        except Exception as exception_error:
            self.logger.error("Error saving: %s", exception_error)
            raise TypeError('An error occurred while saving.') from None

    def update_by_id(self, person_id:str, new_person: ParticipantLeagueRequest) -> ParticipantLeagueResponse:
        try:
            model:ParticipantLeagueModel = self.__participant_league_service.update_by_id(person_id, new_person.to_domain_model(ParticipantLeagueModel))

            if model:
                return ParticipantLeagueResponse().create_by_domain_model(model)

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
