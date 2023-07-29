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
