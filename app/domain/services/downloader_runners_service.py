from ast import List
from app.domain.model.runner_race_detail import RunnerRaceDetail
from app.domain.repository.idownloader_race_data import RaceDownloaderOptions
from app.domain.repository.igeneric_repository import IGenericRepository
from app.domain.services.http_downloader_service import HTTPDownloaderService
from app.domain.services.mappe_runners_factory import MappeRunnersFactory
from scripts.add_runners_into_league import Person

class DownloaderRunnersService:
    def __init__(self, http_service: HTTPDownloaderService, mapper_runners_factory: MappeRunnersFactory):
        self.__http_service = http_service
        self.__mapper_runners_factory = mapper_runners_factory

    def download_runners(self, race_options:RaceDownloaderOptions, person_repository:IGenericRepository):
        response = self.__http_service.get_data(race_options)

        mapper = self.__mapper_runners_factory.factory_method(race_options.type)

        runners:List[RunnerRaceDetail] = []
        filter_by_persons: List[Person] = person_repository.get_all()
        runners = mapper.execute(response, filter_by_persons)

        return runners
