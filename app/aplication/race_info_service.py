from typing import List
from app.core.mapper_utils import dicts_to_class, dicts_to_objects
from app.domain.model.race_info import RaceInfo
from app.domain.model.runner_race_data import RunnerRaceData
from app.domain.services.downloader_runners_service import DownloaderRunnersService
from app.domain.services.http_downloader_service import HTTPDownloaderService
from app.domain.services.mappe_runners_factory import MappeRunnersFactory
from app.domain.services.race_downloader_options_factory import RaceDownloaderOptionsFactory
from app.infrastructure.mongoDB.model.race_data_entity import RaceDataModel
from app.infrastructure.mongoDB.model.runner_race_data_entity_property import RunnerRaceDataEntityProperty
from app.infrastructure.mongoDB.repository.race_info_repository import RaceInfoRepository
from app.infrastructure.repository.repository_utils import load_repository_from_config
from app.infrastructure.rest_api.model.race_info import RaceInfoSimplified, RaceInfoSimplifiedRequest


class RaceInfoService():

    def __init__(self):
        self.__race_info_repository = RaceInfoRepository()
        self.__downloader_runners_service = DownloaderRunnersService(HTTPDownloaderService(), MappeRunnersFactory(), RaceDownloaderOptionsFactory())
        db = load_repository_from_config()
        self.__race_data_repository = db.get_repository('race_data', RaceDataModel)

    def get_all_raw(self) -> List[RaceInfo]:
        all_races_info = self.__race_info_repository.get_all_raw()

        return all_races_info

    def get_all_simplified(self) -> List[RaceInfoSimplified]:
        all_races_info = self.__race_info_repository.get_all_simplified()
        return all_races_info

    def get_simplified_by_id(self, race_id) -> RaceInfoSimplified:
        race = self.__race_info_repository.get_simplified_by_id(race_id)
        return race

    def add_simplified(self, new_race: RaceInfoSimplifiedRequest) -> RaceInfoSimplifiedRequest:
        race_id = self.__race_info_repository.add_simplified(new_race)

        race = self.__race_info_repository.get_simplified_by_id(race_id)

        return race

    def process(self, race_id:str):
        race_info_model:RaceInfoSimplified = self.__race_info_repository.get_simplified_by_id(race_id)

        if race_info_model.race_data_id != '':
            self.__race_data_repository.delete_by_id(race_info_model.race_data_id)

        runners_race_data:List[RunnerRaceData] = self.__downloader_runners_service.get_all_runners(race_info_model)

        runners_race_data_entity = dicts_to_objects(RunnerRaceDataEntityProperty, runners_race_data)
        # new_race_data_entity = RaceDataModel(data=runners_race_data_dict)
        new_race_data_entity = RaceDataModel()
        new_race_data_entity.data = runners_race_data_entity
        new_race_data_id = self.__race_data_repository.add(new_race_data_entity)

        race_info_model.race_data_id = new_race_data_id
        race_info_model.processed = True

        status = self.__race_info_repository.update_by_id(race_info_model.id, race_info_model)

        return race_info_model

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
