from typing import List
from app.domain.model.race_info import RaceInfo
from app.infrastructure.mongoDB.repository.race_info_repository import RaceInfoRepository
from app.infrastructure.rest_api.model.race_info import RaceInfoSimplified


class RaceInfoService():

    def __init__(self):
        self.__race_info_repository = RaceInfoRepository()
        # db = load_repository_from_config()
        # self.__race_data_repository = db.get_repository('race_data', RaceDataModel)

    def get_all_raw(self) -> List[RaceInfo]:
        all_races_info = self.__race_info_repository.get_all_raw()

        return all_races_info

    def get_all_simplified(self) -> List[RaceInfoSimplified]:
        all_races_info = self.__race_info_repository.get_all_simplified()
        return all_races_info

    def get_simplified_by_id(self, race_id) -> RaceInfoSimplified:
        race = self.__race_info_repository.get_simplified_by_id(race_id)
        return race

    def add_simplified(self, new_race: RaceInfoSimplified) -> RaceInfoSimplified:
        race_id = self.__race_info_repository.add_simplified(new_race)

        race = self.__race_info_repository.get_simplified_by_id(race_id)

        return race

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
