from typing import List
from fastapi import File, UploadFile
from app.aplication.base_service import BaseService
from app.aplication.image_service import ImageService
from app.domain.model.person_model import PersonModel
from app.infrastructure.rest_api.controller.base_controller import BaseController
from app.infrastructure.rest_api.model.custom_responses import CustomStaticJSONResponse
from app.infrastructure.rest_api.model.person_model import PersonRequests, PersonResponse


class PersonController(BaseController):
    def __init__(self, base_service:BaseService, model_api_response:PersonResponse, model_domain:PersonModel, image_service:ImageService):
        super().__init__(base_service, model_api_response, model_domain)
        self.image_service = image_service

    def add(self, new_model: PersonRequests, file: UploadFile = File(None)):
        try:
            person_model:PersonModel = new_model.to_domain_model(PersonModel)
            result:PersonModel = self.base_service.add(person_model)

            result.photo_url = self.image_service.upload(result.id, file)

            result:PersonModel = self.base_service.update_by_id(result.id, result)

            if result is None:
                return CustomStaticJSONResponse.error(status_code=404, message='Hubo un error al crear el nuevo item')

            return CustomStaticJSONResponse.success(data=result)
        except Exception as exception_error:
            self.logger.error(f"Error saving: {exception_error}")
            return CustomStaticJSONResponse.invalid_request(status_code=500,errors="Error al processar la peticion")

    def adds(self, new_models: List[PersonRequests]):
        try:
            result_new_models: List[PersonResponse] = []

            for new_model in new_models:
                person_model:PersonModel = new_model.to_domain_model(PersonModel)
                person_model.photo_url = self.image_service.upload(new_model.photo)

                result:PersonModel = self.base_service.add(person_model)

                if result:
                    result_new_models.append(PersonResponse().create_by_domain_model(result))

            return CustomStaticJSONResponse.success(data=result_new_models)
        except Exception as exception_error:
            self.logger.error(f"Error saving: {exception_error}")
            return CustomStaticJSONResponse.invalid_request(status_code=500,errors="Error al processar la peticion")
