import logging
from typing import List
from app.aplication.race_info_service import RaceInfoService
from app.domain.model.race_info_model import RaceInfoRawModel
from app.infrastructure.rest_api.controller.base_controller import BaseController
from app.infrastructure.rest_api.model.race_info import RaceInfoRAW_Response, RaceInfoResponse


class RaceInfoController(BaseController):
    def __init__(self, race_info_repository, domain_model, entity_model, race_info_service:RaceInfoService):
        super().__init__(race_info_repository, domain_model, entity_model)
        self.__race_info_service = race_info_service
        self.logger = logging.getLogger(__name__)

    def get_all_raw(self) -> List[RaceInfoRAW_Response]:
        try:
            results = self.__race_info_service.get_all_raw()
            data_response: List[RaceInfoRAW_Response] = [RaceInfoRAW_Response().create_by_domain_model(result) for result in results]

            return data_response
        except Exception as exception_error:
            self.logger.error("Error retrieving all items: %s", exception_error)
            raise TypeError('An error occurred while retrieving all items.') from None

    def get_raw_by_id(self, race_id: str) -> RaceInfoRAW_Response:
        try:
            result:RaceInfoRawModel = self.__race_info_service.get_raw_by_id(race_id)
            data_response = RaceInfoRAW_Response().create_by_domain_model(result)

            return data_response
        except Exception as exception_error:
            self.logger.error("Error retrieving all items: %s", exception_error)
            raise TypeError('An error occurred while retrieving all items.') from None

    def run_process(self, race_id) -> RaceInfoResponse:
        try:
            model = self.__race_info_service.process(race_id)

            if model:
                return RaceInfoResponse().create_by_domain_model(model)

            return {}
        except Exception as exception_error:
            self.logger.error("Error deleting: %s", exception_error)
            raise TypeError('An error occurred while deleting.') from None
