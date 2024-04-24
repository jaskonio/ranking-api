from typing import List
from app.domain.model.race_info import RaceInfo
from app.infrastructure.mongoDB.repository.race_info_repository import RaceInfoRepository

class RaceInfoService():

    def __init__(self):
        self.__race_info_repository = RaceInfoRepository()

    def get_all(self) -> List[RaceInfo]:
        all_races_info = self.__race_info_repository.get_all()

        return all_races_info

    # def get_by_id(self, race_id) -> RaceBase:
    #     race = self.__race_repository.get_by_id(race_id)
    #     return race

    # def add(self, new_race: RaceBase) -> RaceBase:
    #     race_id = self.__race_repository.add(new_race)

    #     race = self.__race_repository.get_by_id(race_id)

    #     return race

    # def process(self, race_id:str):
    #     race:RaceBase = self.__race_repository.get_by_id(race_id)

    #     runners:List[RunnerRaceRanking] = self.__downloader_runners_service.get_runners_by_persons(race, self.__person_repository.get_all())

    #     race.set_raw_ranking(runners)

    #     status = self.__race_repository.update_by_id(race.id, race)

    #     if status:
    #         race = self.__race_repository.get_by_id(race.id)
    #         return race
    #     else:
    #         return None

    # def update_by_id(self, race_id:str, new_race:RaceBase):
    #     status = self.__race_repository.update_by_id(race_id, new_race)

    #     if status:
    #         race = self.__race_repository.get_by_id(race_id)
    #         return race
    #     else:
    #         return None

    # def delete_by_id(self, race_id):
    #     status = self.__race_repository.delete_by_id(race_id)

    #     if status:
    #         return status

    #     return None
