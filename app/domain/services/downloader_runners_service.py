from typing import List
from app.domain.model.race import Race
from app.domain.model.runner_race_ranking import RunnerRaceRanking
from app.domain.services.http_downloader_service import HTTPDownloaderService
from app.domain.services.mappe_runners_factory import MappeRunnersFactory
from app.domain.model.person import Person
from app.domain.services.race_downloader_options_factory import RaceDownloaderOptionsFactory

class DownloaderRunnersService:
    def __init__(self, http_service: HTTPDownloaderService, mapper_runners_factory: MappeRunnersFactory, race_downloader_options_factory:RaceDownloaderOptionsFactory):
        self.__http_service = http_service
        self.__mapper_runners_factory = mapper_runners_factory
        self.__race_downloader_options_factory = race_downloader_options_factory

    def get_all_runners(self, race: Race):
        try:
            race_options = self.__race_downloader_options_factory.factory_method(race)

            response = self.__http_service.get_data(race_options)

            mapper = self.__mapper_runners_factory.factory_method(race_options.type)

            runners = mapper.execute(response)

            return runners
        except Exception as e:
            return []

    def get_runners_by_persons(self, race: Race, persons: List[Person]):
        all_runners = self.get_all_runners(race)

        runners:List[RunnerRaceRanking] = []

        for runner in all_runners:
            if runner in persons:
                runners.append(runner)

        return runners
