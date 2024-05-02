import logging
from typing import List
from app.aplication.league_service import LeagueService
from app.domain.model.league_model import LeagueRAWModel
from app.infrastructure.rest_api.controller.base_controller import BaseController
from app.infrastructure.rest_api.model.custom_responses import CustomStaticJSONResponse
from app.infrastructure.rest_api.model.league_model import LeagueRawResponse


class LeagueController(BaseController):
    def __init__(self, league_service:LeagueService, api_model, domain_model):
        super().__init__(league_service, api_model, domain_model)
        self.logger = logging.getLogger(__name__)
        self.__league_service = league_service

    def get_all_raw(self):
        try:
            models: List[LeagueRAWModel] = self.__league_service.get_all_raw()
            results = [LeagueRawResponse().create_by_domain_model(model) for model in models]
            return CustomStaticJSONResponse.success(data=results)
        except Exception as exception_error:
            self.logger.error("Error retrieving all items: %s", exception_error)
            return CustomStaticJSONResponse.invalid_request(status_code=500,errors="Error al processar la peticion")

    def get_raw_by_id(self, league_id:str):
        try:
            league_model = self.__league_service.get_raw_by_id(league_id)

            if league_model is None:
                return CustomStaticJSONResponse.error(status_code=404, message=f"El ID {league_id} no se ha encontrado")

            return CustomStaticJSONResponse.success(data=self.model_api_response().create_by_domain_model(league_model))
        except Exception as exception_error:
            self.logger.error("Error retrieving item: %s", exception_error)
            return CustomStaticJSONResponse.invalid_request(status_code=500,errors="Error al processar la peticion")

    def run_process_by_id(self, league_id:str) -> LeagueRawResponse:
        try:
            league_model = self.__league_service.run_process(league_id)

            if league_model:
                return CustomStaticJSONResponse.error(status_code=404, message=f"El ID {league_id} no se ha encontrado")

            return CustomStaticJSONResponse.success(data=self.model_api_response().create_by_domain_model(league_model))
        except Exception as exception_error:
            self.logger.error("Error retrieving item: %s", exception_error)
            return CustomStaticJSONResponse.invalid_request(status_code=500,errors="Error al processar la peticion")
