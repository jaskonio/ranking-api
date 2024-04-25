import logging
from app.aplication.season_service import SeasonService
from app.domain.model.season_model import SeasonModel
from app.infrastructure.rest_api.model.season_info import API_SeasonRequest, API_SeasonResponse


class SeasonController():
    def __init__(self, season_service:SeasonService):
        self.__season_service = season_service
        self.logger = logging.getLogger(__name__)

    def get_all(self) -> list[API_SeasonResponse]:
        try:
            models = self.__season_service.get_all()
            return [API_SeasonResponse().create_by_domain_model(model) for model in models]
        except Exception as exception_error:
            self.logger.error("Error retrieving all items: %s", exception_error)
            raise TypeError('An error occurred while retrieving all items.') from None

    def get_by_id(self, season_id:str) -> API_SeasonResponse:
        try:
            model = self.__season_service.get_by_id(season_id)

            if model:
                return API_SeasonResponse().create_by_domain_model(model)

            return {}
        except Exception as exception_error:
            self.logger.error("Error retrieving item: %s", exception_error)
            raise TypeError('An error occurred while retrieving item.') from None

    def add(self, season_api_model:API_SeasonRequest) -> API_SeasonResponse:
        try:
            model = season_api_model.to_domain_model(SeasonModel)
            season_model = self.__season_service.add(model)

            if season_model:
                return API_SeasonResponse().create_by_domain_model(season_model)

            return {}
        except Exception as exception_error:
            self.logger.error("Error saving: %s", exception_error)
            raise TypeError('An error occurred while saving.') from None

    def update_by_id(self, season_id:str, new_season_model:API_SeasonRequest) -> API_SeasonResponse:
        try:
            model = self.__season_service.update_by_id(season_id, new_season_model.to_domain_model(SeasonModel))

            if model:
                return API_SeasonResponse().create_by_domain_model(model)

            return {}
        except Exception as exception_error:
            self.logger.error("Error updating: %s", exception_error)
            raise TypeError('An error occurred while updating.') from None

    def delete_by_id(self, season_id:str):
        try:
            status = self.__season_service.delete_by_id(season_id)

            if status:
                return status

            return {}
        except Exception as exception_error:
            self.logger.error("Error deleting: %s", exception_error)
            raise TypeError('An error occurred while deleting.') from None
