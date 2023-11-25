from typing import List
from app.domain.model.runner_race_ranking import RunnerRaceRanking
from app.domain.repository.idownloader_race_data import RaceDownloaderOptions
from app.domain.services.http_downloader_service import HTTPDownloaderService
from app.domain.services.mappe_runners_factory import MappeRunnersFactory
from app.domain.model.person import Person

class DownloaderRunnersService:
    def __init__(self, http_service: HTTPDownloaderService, mapper_runners_factory: MappeRunnersFactory):
        self.__http_service = http_service
        self.__mapper_runners_factory = mapper_runners_factory

    def get_all_runners(self, race_options:RaceDownloaderOptions):
        response = self.__http_service.get_data(race_options)

        mapper = self.__mapper_runners_factory.factory_method(race_options.type)

        runners = mapper.execute(response)

        return runners

    def get_runners_by_persons(self, race_options: RaceDownloaderOptions, persons: List[Person]):
        all_runners = self.get_all_runners(race_options)

        runners:List[RunnerRaceRanking] = []

        for runner in all_runners:
            if runner in persons:
                runners.append(runner)

        return runners
