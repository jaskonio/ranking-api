import logging
from typing import List, Optional
from app.aplication.base_service import BaseService
from app.domain.model.person_model import PersonModel
from app.infrastructure.rest_api.model.custom_responses import CustomStaticJSONResponse
from app.infrastructure.rest_api.model.person_model import PersonRequests, PersonResponse


class PersonController():
    def __init__(self, person_service:BaseService):
        self.__person_service = person_service
        self.logger = logging.getLogger(__name__)

    def get_all(self) -> List[PersonResponse]:
        try:
            models: List[PersonModel] = self.__person_service.get_all()
            models = [PersonResponse().create_by_domain_model(model) for model in models]
            return CustomStaticJSONResponse.success(data=models)
        except Exception as exception_error:
            self.logger.error("Error retrieving all items: %s", exception_error)
            return CustomStaticJSONResponse.invalid_request(status_code=500,errors="Error al processar la peticion")

    def get_by_id(self, person_id:str) -> Optional[PersonResponse]:
        try:
            model:PersonModel = self.__person_service.get_by_id(person_id)

            if model is None:
                return CustomStaticJSONResponse.error(status_code=404, message=f"El ID {person_id} no se ha encontrado")

            return CustomStaticJSONResponse.success(data=PersonResponse().create_by_domain_model(model))
        except Exception as exception_error:
            self.logger.error("Error retrieving item: %s", exception_error)
            return CustomStaticJSONResponse.invalid_request(status_code=500,errors="Error al processar la peticion")

    def add(self, new_person: PersonRequests) -> Optional[PersonResponse]:
        try:
            new_person.photo_url = 'https://i.pravatar.cc/30'
            model:PersonModel = self.__person_service.add(new_person.to_domain_model(PersonModel))

            if model:
                return PersonResponse().create_by_domain_model(model)

            return None
        except Exception as exception_error:
            self.logger.error("Error saving: %s", exception_error)
            raise TypeError('An error occurred while saving.') from None

    def adds(self, new_persons: PersonRequests) -> List[PersonResponse]:
        try:
            result_new_persons: List[PersonResponse] = []
            for new_person in new_persons:
                new_person.photo_url = 'https://i.pravatar.cc/30'
                model:PersonModel = self.__person_service.add(new_person.to_domain_model(PersonModel))
                if model:
                    result_new_persons.append(PersonResponse().create_by_domain_model(model))
            return CustomStaticJSONResponse.success(data=result_new_persons)
        except Exception as exception_error:
            self.logger.error("Error saving: %s", exception_error)
            return CustomStaticJSONResponse.invalid_request(status_code=500,errors="Error al processar la peticion")

    def update_by_id(self, person_id:str, new_person: PersonRequests) -> Optional[PersonResponse]:
        try:
            model:PersonModel = self.__person_service.update_by_id(person_id, new_person.to_domain_model(PersonModel))

            if model is None:
                return CustomStaticJSONResponse.error(status_code=404, message=f"El ID {person_id} no se ha encontrado")

            return CustomStaticJSONResponse.success(data=PersonResponse().create_by_domain_model(model))
        except Exception as exception_error:
            self.logger.error("Error updating: %s", exception_error)
            return CustomStaticJSONResponse.invalid_request(status_code=500,errors="Error al processar la peticion")

    def delete_by_id(self, person_id:str) -> bool:
        try:
            status = self.__person_service.delete_by_id(person_id)

            return status
        except Exception as exception_error:
            self.logger.error("Error deleting: %s", exception_error)
            return CustomStaticJSONResponse.invalid_request(status_code=500,errors="Error al processar la peticion")
