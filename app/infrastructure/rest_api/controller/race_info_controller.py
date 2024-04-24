import logging
from typing import List
from app.aplication.race_info_service import RaceInfoService
from app.infrastructure.rest_api.model.race_info import RaceInfoSimplified


class RaceInfoController():
    def __init__(self, race_info_service:RaceInfoService):
        self.__race_info_service = race_info_service
        self.logger = logging.getLogger(__name__)

    def get_all_raw(self):
        try:
            return self.__race_info_service.get_all_raw()
        except Exception as exception_error:
            self.logger.error("Error retrieving all items: %s", exception_error)
            raise TypeError('An error occurred while retrieving all items.') from None

    def get_all_simplified(self):
        try:
            return self.__race_info_service.get_all_simplified()
        except Exception as exception_error:
            self.logger.error("Error retrieving all items: %s", exception_error)
            raise TypeError('An error occurred while retrieving all items.') from None

    def get_simplified_by_id(self, race_id):
        try:
            race = self.__race_info_service.get_simplified_by_id(race_id)

            if race:
                return race

            return {}
        except Exception as exception_error:
            self.logger.error("Error retrieving item: %s", exception_error)
            raise TypeError('An error occurred while retrieving item.') from None

    def add_simplified(self, race:RaceInfoSimplified):
        try:
            race = self.__race_info_service.add_simplified(race)

            if race:
                return race

            return {}
        except Exception as exception_error:
            self.logger.error("Error saving: %s", exception_error)
            raise TypeError('An error occurred while saving.') from None

    # def update_by_id(self, race_id:str, new_race):
    #     try:
    #         race = self.__race_info_service.update_by_id(race_id, new_race)

    #         if race:
    #             return race

    #         return {}
    #     except Exception as exception_error:
    #         self.logger.error("Error updating: %s", exception_error)
    #         raise TypeError('An error occurred while updating.') from None

    # def delete_by_id(self, race_id):
    #     try:
    #         status = self.__race_info_service.delete_by_id(race_id)

    #         if status:
    #             return status

    #         return {}
    #     except Exception as exception_error:
    #         self.logger.error("Error deleting: %s", exception_error)
    #         raise TypeError('An error occurred while deleting.') from None

    # def run(self, race_id):
    #     try:
    #         status = self.__race_info_service.process(race_id)

    #         if status:
    #             return status

    #         return {}
    #     except Exception as exception_error:
    #         self.logger.error("Error deleting: %s", exception_error)
    #         raise TypeError('An error occurred while deleting.') from None
