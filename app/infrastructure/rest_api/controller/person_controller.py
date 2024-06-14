import logging
from typing import List
from app.aplication.iservice import IGenericService
from app.domain.model.person_model import PersonModel
from app.infrastructure.cloud.aws_repository import AWS_Repository
from app.infrastructure.rest_api.controller.base_controller import BaseController
from app.infrastructure.rest_api.model.custom_responses import CustomStaticJSONResponse

class PersonController(BaseController):
    def __init__(self, person_service:IGenericService, api_model, domain_model, image_service: AWS_Repository):
        super().__init__(person_service, api_model, domain_model)
        self.logger = logging.getLogger(__name__)
        self.__image_service = image_service

    def delete_by_id(self, model_id: str):
        try:
            model:PersonModel = self.base_service.get_by_id(model_id)

            if model.photo_url != "":
                self.__image_service.remove_file(model.photo_url)

            domain_model = self.base_service.delete_by_id(model_id)

            if domain_model is False:
                return CustomStaticJSONResponse.error(status_code=404, message=f"El ID {model_id} no se ha encontrado")

            return CustomStaticJSONResponse.success(data= {"success" : True})
        except Exception as exception_error:
            self.logger.error("Error updating: %s", exception_error)
            return CustomStaticJSONResponse.invalid_request(status_code=500,errors="Error al processar la peticion")
