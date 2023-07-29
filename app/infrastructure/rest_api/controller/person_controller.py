import logging
from app.aplication.person_service import PersonService


class PersonController():
    def __init__(self, person_service:PersonService):
        self.__person_service = person_service
        self.logger = logging.getLogger(__name__)

    def get_all(self):
        try:
            return self.__person_service.get_all()
        except Exception as exception_error:
            self.logger.error("Error retrieving all items: %s", exception_error)
            raise TypeError('An error occurred while retrieving all items.') from None

    def get_by_id(self, person_id):
        try:
            person = self.__person_service.get_by_id(person_id)

            if person:
                return person

            return {}
        except Exception as exception_error:
            self.logger.error("Error retrieving item: %s", exception_error)
            raise TypeError('An error occurred while retrieving item.') from None

    def add(self, person):
        try:
            return self.__person_service.add(person)
        except Exception as exception_error:
            self.logger.error("Error saving: %s", exception_error)
            raise TypeError('An error occurred while saving.') from None

    def update_by_id(self, person_id:str, new_person):
        try:
            return self.__person_service.update_by_id(person_id, new_person)
        except Exception as exception_error:
            self.logger.error("Error updating: %s", exception_error)
            raise TypeError('An error occurred while updating.') from None

    def delete_by_id(self, person_id):
        try:
            return self.__person_service.delete_by_id(person_id)
        except Exception as exception_error:
            self.logger.error("Error deleting: %s", exception_error)
            raise TypeError('An error occurred while deleting.') from None
