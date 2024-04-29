import logging
from typing import List
from app.aplication.race_info_service import RaceInfoService
from app.domain.model.race_info_model import RaceInfoRawModel, RaceInfoModel
from app.infrastructure.rest_api.model.race_info import RaceInfoRAW_Response, RaceInfoRequest, RaceInfoResponse


class RaceInfoController():
    def __init__(self, race_info_service:RaceInfoService):
        self.__race_info_service = race_info_service
        self.logger = logging.getLogger(__name__)

    def get_all_raw(self) -> List[RaceInfoRAW_Response]:
        try:
            results = self.__race_info_service.get_all_raw()
            data_response: List[RaceInfoRAW_Response] = [RaceInfoRAW_Response().create_by_domain_model(result) for result in results]

            return data_response
        except Exception as exception_error:
            self.logger.error("Error retrieving all items: %s", exception_error)
            raise TypeError('An error occurred while retrieving all items.') from None

    def get_raw_by_id(self, race_id: str) -> RaceInfoRAW_Response:
        try:
            result:RaceInfoRawModel = self.__race_info_service.get_raw_by_id(race_id)
            data_response = RaceInfoRAW_Response().create_by_domain_model(result)

            return data_response
        except Exception as exception_error:
            self.logger.error("Error retrieving all items: %s", exception_error)
            raise TypeError('An error occurred while retrieving all items.') from None

    def get_all(self) -> List[RaceInfoResponse]:
        try:
            results = self.__race_info_service.get_all()
            results = [RaceInfoResponse().create_by_domain_model(result) for result in results]
            return results
        except Exception as exception_error:
            self.logger.error("Error retrieving all items: %s", exception_error)
            raise TypeError('An error occurred while retrieving all items.') from None

    def get_by_id(self, race_id) -> RaceInfoResponse:
        try:
            race = self.__race_info_service.get_by_id(race_id)

            if race:
                return RaceInfoResponse().create_by_domain_model(race)

            return {}
        except Exception as exception_error:
            self.logger.error("Error retrieving item: %s", exception_error)
            raise TypeError('An error occurred while retrieving item.') from None

    def add(self, race:RaceInfoRequest) -> RaceInfoResponse:
        try:
            race = self.__race_info_service.add(race.to_domain_model(RaceInfoModel))

            if race:
                return RaceInfoResponse().create_by_domain_model(race)

            return {}
        except Exception as exception_error:
            self.logger.error("Error saving: %s", exception_error)
            raise TypeError('An error occurred while saving.') from None

    def run_process(self, race_id) -> RaceInfoResponse:
        try:
            model = self.__race_info_service.process(race_id)

            if model:
                return RaceInfoResponse().create_by_domain_model(model)

            return {}
        except Exception as exception_error:
            self.logger.error("Error deleting: %s", exception_error)
            raise TypeError('An error occurred while deleting.') from None

    def update_by_id(self, race_id:str, new_race):
        try:
            race = self.__race_info_service.update_by_id(race_id, new_race)

            if race:
                return race

            return {}
        except Exception as exception_error:
            self.logger.error("Error updating: %s", exception_error)
            raise TypeError('An error occurred while updating.') from None

    def delete_by_id(self, race_id):
        try:
            status = self.__race_info_service.delete_by_id(race_id)

            if status:
                return status

            return {}
        except Exception as exception_error:
            self.logger.error("Error deleting: %s", exception_error)
            raise TypeError('An error occurred while deleting.') from None
