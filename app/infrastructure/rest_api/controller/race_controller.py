import logging
from app.aplication.race_service import RaceService


class RaceController():
    def __init__(self, race_service:RaceService):
        self.__race_service = race_service
        self.logger = logging.getLogger(__name__)

    def get_all(self):
        try:
            return self.__race_service.get_all()
        except Exception as exception_error:
            self.logger.error("Error retrieving all items: %s", exception_error)
            raise TypeError('An error occurred while retrieving all items.') from None

    def get_by_id(self, race_id):
        try:
            race = self.__race_service.get_by_id(race_id)

            if race:
                return race

            return {}
        except Exception as exception_error:
            self.logger.error("Error retrieving item: %s", exception_error)
            raise TypeError('An error occurred while retrieving item.') from None

    def add(self, race):
        try:
            race = self.__race_service.add(race)

            if race:
                return race

            return {}
        except Exception as exception_error:
            self.logger.error("Error saving: %s", exception_error)
            raise TypeError('An error occurred while saving.') from None

    def update_by_id(self, race_id:str, new_race):
        try:
            race = self.__race_service.update_by_id(race_id, new_race)

            if race:
                return race

            return {}
        except Exception as exception_error:
            self.logger.error("Error updating: %s", exception_error)
            raise TypeError('An error occurred while updating.') from None

    def delete_by_id(self, race_id):
        try:
            status = self.__race_service.delete_by_id(race_id)

            if status:
                return status

            return {}
        except Exception as exception_error:
            self.logger.error("Error deleting: %s", exception_error)
            raise TypeError('An error occurred while deleting.') from None

    def run(self, race_id):
        try:
            status = self.__race_service.process(race_id)

            if status:
                return status

            return {}
        except Exception as exception_error:
            self.logger.error("Error deleting: %s", exception_error)
            raise TypeError('An error occurred while deleting.') from None
