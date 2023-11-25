from typing import List
from app.domain.model.race import Race
from app.domain.model.runner_race_ranking import RunnerRaceRanking
from app.domain.repository.idownloader_race_data import RaceDownloaderOptions
from app.domain.repository.igeneric_repository import IGenericRepository
from app.domain.services.downloader_runners_service import DownloaderRunnersService

class RaceService():

    def __init__(self, race_repository:IGenericRepository, person_repository:IGenericRepository
                 , downloader_runners_service:DownloaderRunnersService):
        self.__race_repository = race_repository
        self.__person_repository = person_repository
        self.__downloader_runners_service = downloader_runners_service

    def get_all(self) -> List[Race]:
        races = self.__race_repository.get_all()

        return races

    def get_by_id(self, race_id) -> Race:
        race = self.__race_repository.get_by_id(race_id)

        return race

    def add(self, race_options: RaceDownloaderOptions) -> Race:
        race = Race(id=0, name=race_options.race_name, url=race_options.url)

        if not race_options.is_sorted:
            runners:List[RunnerRaceRanking] = self.__downloader_runners_service.get_runners_by_persons(race_options, self.__person_repository.get_all())
            race.set_raw_ranking(runners)

        race_id = self.__race_repository.add(race)

        race = self.__race_repository.get_by_id(race_id)

        return race

    def update_by_id(self, race_id:str, new_race):
        if not new_race.is_sorted:
            runners:List[RunnerRaceRanking] = self.__downloader_runners_service.download_race_data(new_race.url, self.__person_repository)
            new_race.set_ranking(runners)

        status = self.__race_repository.update_by_id(race_id, new_race)

        if status:
            race = self.__race_repository.get_by_id(race_id)
            return race
        else:
            return None

    def delete_by_id(self, race_id):
        status = self.__race_repository.delete_by_id(race_id)

        if status:
            return status

        return None
