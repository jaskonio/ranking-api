import logging
from typing import List
from app.aplication.person_service import PersonService
from app.domain.model.person_model import PersonModel
from app.infrastructure.rest_api.model.person_model import PersonRequests, PersonResponse


class PersonController():
    def __init__(self, person_service:PersonService):
        self.__person_service = person_service
        self.logger = logging.getLogger(__name__)

    def get_all(self) -> List[PersonResponse]:
        try:
            models: List[PersonModel] = self.__person_service.get_all()
            return [PersonResponse().create_by_domain_model(model) for model in models]
        except Exception as exception_error:
            self.logger.error("Error retrieving all items: %s", exception_error)
            raise TypeError('An error occurred while retrieving all items.') from None

    def get_by_id(self, person_id:str) -> PersonResponse:
        try:
            model:PersonModel = self.__person_service.get_by_id(person_id)

            if model:
                return PersonResponse().create_by_domain_model(model)

            return {}
        except Exception as exception_error:
            self.logger.error("Error retrieving item: %s", exception_error)
            raise TypeError('An error occurred while retrieving item.') from None

    def add(self, new_person: PersonRequests) -> PersonResponse:
        try:
            model:PersonModel = self.__person_service.add(new_person.to_domain_model(PersonModel))

            if model:
                return PersonResponse().create_by_domain_model(model)

            return {}
        except Exception as exception_error:
            self.logger.error("Error saving: %s", exception_error)
            raise TypeError('An error occurred while saving.') from None

    def update_by_id(self, person_id:str, new_person: PersonRequests) -> PersonResponse:
        try:
            model:PersonModel = self.__person_service.update_by_id(person_id, new_person.to_domain_model(PersonModel))

            if model:
                return PersonResponse().create_by_domain_model(model)

            return {}
        except Exception as exception_error:
            self.logger.error("Error updating: %s", exception_error)
            raise TypeError('An error occurred while updating.') from None

    def delete_by_id(self, person_id:str) -> bool:
        try:
            status = self.__person_service.delete_by_id(person_id)

            if status:
                return status

            return {}
        except Exception as exception_error:
            self.logger.error("Error deleting: %s", exception_error)
            raise TypeError('An error occurred while deleting.') from None
