import logging
from typing import List
from app.domain.model.race_info_model import RaceInfoModel
from app.domain.model.runner_race_data_model import RunnerRaceDataModel
from app.domain.services.http_downloader_service import HTTPDownloaderService
from app.domain.services.mappe_runners_factory import MappeRunnersFactory
# from app.domain.model.person_model import PersonModel
from app.domain.services.race_downloader_options_factory import RaceDownloaderOptionsFactory


class DownloaderRunnersService:
    def __init__(self, http_service: HTTPDownloaderService, mapper_runners_factory: MappeRunnersFactory, race_downloader_options_factory:RaceDownloaderOptionsFactory):
        self.__http_service = http_service
        self.__mapper_runners_factory = mapper_runners_factory
        self.__race_downloader_options_factory = race_downloader_options_factory

        self.logger = logging.getLogger(__name__)

    def get_all_runners(self, race_info_simplified_model: RaceInfoModel) -> List[RunnerRaceDataModel]:
        try:
            race_options = self.__race_downloader_options_factory.factory_method(race_info_simplified_model)

            response = self.__http_service.get_data(race_options)

            mapper = self.__mapper_runners_factory.factory_method(race_options)

            runners = mapper.execute(response)

            return runners
        except Exception as exception_error:
            self.logger.error("Error retrieving item: %s", exception_error)
            raise TypeError('An error occurred while get_all_runners') from None
