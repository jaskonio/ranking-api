from typing import List
from app.aplication.DownloaderService import DownloaderService
from app.domain.model.race import Race
from app.domain.model.runner_race_detail import RunnerRaceDetail
from app.domain.repository.igeneric_repository import IGenericRepository


class RaceService():

    def __init__(self, race_repository:IGenericRepository, downloader_service:DownloaderService):
        self.__race_repository = race_repository
        self.__downloader_service = downloader_service

    def get_all(self) -> List[Race]:
        races = self.__race_repository.get_all()

        return races

    def get_by_id(self, race_id) -> Race:
        race = self.__race_repository.get_by_id(race_id)

        return race

    def add(self, race: Race) -> Race:
        if not race.is_sorted:
            runners:List[RunnerRaceDetail] = self.__downloader_service.download_race_data(race.url)
            race.set_ranking(runners)

        race_id = self.__race_repository.add(race)

        race = self.__race_repository.get_by_id(race_id)

        return race

    def update_by_id(self, race_id:str, new_race):
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
