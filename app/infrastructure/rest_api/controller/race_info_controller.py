import logging
from typing import List
from app.aplication.race_info_service import RaceInfoService
from app.domain.model.race_info_model import RaceModel
from app.infrastructure.rest_api.controller.base_controller import BaseController
from app.infrastructure.rest_api.model.custom_responses import CustomStaticJSONResponse
from app.infrastructure.rest_api.model.race_info import RaceInfoRAW_Response, RaceInfoResponse


class RaceInfoController(BaseController):
    def __init__(self, race_info_service:RaceInfoService, domain_model, entity_model):
        super().__init__(race_info_service, domain_model, entity_model)
        self.logger = logging.getLogger(__name__)

    def get_all_raw(self) -> List[RaceInfoRAW_Response]:
        try:
            results = self.base_service.get_all_raw()
            data_response: List[RaceInfoRAW_Response] = [RaceInfoRAW_Response().create_by_domain_model(result) for result in results]

            return CustomStaticJSONResponse.success(data=data_response)
        except Exception as exception_error:
            self.logger.error("Error retrieving all items: %s", exception_error)
            return CustomStaticJSONResponse.invalid_request(status_code=500,errors="Error al processar la peticion")

    def get_raw_by_id(self, race_id: str) -> RaceInfoRAW_Response:
        try:
            result:RaceModel = self.base_service.get_raw_by_id(race_id)
            data_response = RaceInfoRAW_Response().create_by_domain_model(result)

            if data_response is None:
                return CustomStaticJSONResponse.error(status_code=404, message=f"El ID {race_id} no se ha encontrado")

            return CustomStaticJSONResponse.success(data=data_response)
        except Exception as exception_error:
            self.logger.error("Error retrieving all items: %s", exception_error)
            return CustomStaticJSONResponse.invalid_request(status_code=500,errors="Error al processar la peticion")

    def run_process(self, race_id) -> RaceInfoResponse:
        try:
            model = self.base_service.process(race_id)

            if model is None:
                return CustomStaticJSONResponse.error(status_code=404, message=f"El ID {race_id} no se ha encontrado")

            return CustomStaticJSONResponse.success(data=model)
        except Exception as exception_error:
            self.logger.error("Error processing: %s", exception_error)
            return CustomStaticJSONResponse.invalid_request(status_code=500,errors="Error al processar la peticion")
