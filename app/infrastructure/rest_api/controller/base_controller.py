import logging
from pydantic import BaseModel
from app.aplication.base_service import BaseService
from app.infrastructure.rest_api.controller.ibase_controller import IBaseController
from app.infrastructure.rest_api.model.base_api_model import BaseAPI_Model
from app.infrastructure.rest_api.model.custom_responses import CustomStaticJSONResponse


class BaseController(IBaseController):
    def __init__(self, base_service:BaseService, model_api_response:BaseAPI_Model, model_domain:BaseModel):
        self.logger = logging.getLogger(__name__)
        self.base_service = base_service
        self.model_api_response = model_api_response
        self.model_domain = model_domain

    def get_all(self):
        try:
            results = self.base_service.get_all()
            results = [self.model_api_response().create_by_domain_model(result) for result in results]
            return CustomStaticJSONResponse.success(data=results)
        except Exception as exception_error:
            self.logger.error("Error retrieving all items: %s", exception_error)
            return CustomStaticJSONResponse.invalid_request(status_code=500,errors="Error al processar la peticion")

    def get_by_id(self, model_id):
        try:
            result_model_domain:BaseModel = self.base_service.get_by_id(model_id)

            if result_model_domain is None:
                return CustomStaticJSONResponse.error(status_code=404, message=f"El ID {model_id} no se ha encontrado")

            return CustomStaticJSONResponse.success(data=self.model_api_response().create_by_domain_model(result_model_domain))
        except Exception as exception_error:
            self.logger.error("Error retrieving item: %s", exception_error)
            return CustomStaticJSONResponse.invalid_request(status_code=500,errors="Error al processar la peticion")

    def add(self, new_model:BaseAPI_Model):
        try:
            result_model_domain = self.base_service.add(new_model.to_domain_model(self.model_domain))

            if result_model_domain is None:
                return CustomStaticJSONResponse.error(status_code=404, message='Hubo un error al crear el nuevo item')

            return CustomStaticJSONResponse.success(data=self.model_api_response().create_by_domain_model(result_model_domain))
        except Exception as exception_error:
            self.logger.error("Error saving: %s", exception_error)
            return CustomStaticJSONResponse.invalid_request(status_code=500,errors="Error al processar la peticion")

    def update_by_id(self, model_id:str, new_model: BaseAPI_Model):
        try:
            result_model_domain = self.base_service.update_by_id(model_id, new_model.to_domain_model(self.model_domain))

            if result_model_domain is None:
                return CustomStaticJSONResponse.error(status_code=404, message=f"El ID {model_id} no se ha encontrado")

            return CustomStaticJSONResponse.success(data=self.model_api_response().create_by_domain_model(result_model_domain))
        except Exception as exception_error:
            self.logger.error("Error updating: %s", exception_error)
            return CustomStaticJSONResponse.invalid_request(status_code=500,errors="Error al processar la peticion")

    def delete_by_id(self, model_id):
        try:
            status = self.base_service.delete_by_id(model_id)

            return status
        except Exception as exception_error:
            self.logger.error("Error deleting: %s", exception_error)
            return CustomStaticJSONResponse.invalid_request(status_code=500,errors="Error al processar la peticion")
