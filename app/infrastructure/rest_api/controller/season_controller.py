import operator
from typing import List
from app.aplication.base_service import BaseService
from app.domain.model.season_model import SeasonModel
from app.infrastructure.rest_api.controller.base_controller import BaseController
from app.infrastructure.rest_api.model.custom_responses import CustomStaticJSONResponse
from app.infrastructure.rest_api.model.season_info import SeasonRawResponse, SeasonResponse


class SeasonController(BaseController):
    def __init__(self, base_service:BaseService, model_api_response:SeasonResponse, model_domain:SeasonModel):
        super().__init__(base_service, model_api_response, model_domain)

    def get_all(self):
        try:
            results:List[SeasonResponse] = self.base_service.get_all()
            
            new_results_ordered = sorted(results, key=operator.attrgetter('order'), reverse=True)
            for s in new_results_ordered:
                if s.order == -1:
                    new_results_ordered.remove(s)
                    new_results_ordered.insert(0, s)

            results = [SeasonResponse().create_by_domain_model(result) for result in new_results_ordered]
            return CustomStaticJSONResponse.success(data=results)
        except Exception as exception_error:
            self.logger.error("Error retrieving all items: %s", exception_error)
            return CustomStaticJSONResponse.invalid_request(status_code=500,errors="Error al processar la peticion")