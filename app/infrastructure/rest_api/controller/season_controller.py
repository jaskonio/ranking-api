from app.aplication.base_service import BaseService
from app.domain.model.season_model import SeasonModel
from app.infrastructure.rest_api.controller.base_controller import BaseController
from app.infrastructure.rest_api.model.custom_responses import CustomStaticJSONResponse
from app.infrastructure.rest_api.model.season_info import SeasonRawResponse, SeasonResponse


class SeasonController(BaseController):
    def __init__(self, base_service:BaseService, model_api_response:SeasonResponse, model_domain:SeasonModel):
        super().__init__(base_service, model_api_response, model_domain)

    def get_all_raw(self):
        try:
            results = self.base_service.get_all_raw()
            results = [SeasonRawResponse().create_by_domain_model(result) for result in results]
            return CustomStaticJSONResponse.success(data=results)
        except Exception as exception_error:
            self.logger.error("Error retrieving all items: %s", exception_error)
            return CustomStaticJSONResponse.invalid_request(status_code=500,errors="Error al processar la peticion")

    def get_raw_by_id(self, season_id:str):
        try:
            result_model_domain = self.base_service.get_raw_by_id(season_id)

            if result_model_domain is None:
                return CustomStaticJSONResponse.error(status_code=404, message=f"El ID {season_id} no se ha encontrado")

            return CustomStaticJSONResponse.success(data=SeasonRawResponse().create_by_domain_model(result_model_domain))
        except Exception as exception_error:
            self.logger.error("Error retrieving item: %s", exception_error)
            return CustomStaticJSONResponse.invalid_request(status_code=500,errors="Error al processar la peticion")
