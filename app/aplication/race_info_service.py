from typing import List
from app.domain.model.race_data_model import RaceDataModel
from app.domain.model.race_info_model import RaceInfoRawModel, RaceInfoModel
from app.domain.model.runner_race_data_model import RunnerRaceDataModel
from app.domain.services.downloader_runners_service import DownloaderRunnersService
from app.domain.services.http_downloader_service import HTTPDownloaderService
from app.domain.services.mappe_runners_factory import MappeRunnersFactory
from app.domain.services.race_downloader_options_factory import RaceDownloaderOptionsFactory
from app.infrastructure.mongoDB.model.race_data_entity import RaceDataEntity
from app.infrastructure.mongoDB.model.race_info_entity import RaceInfoEntity
from app.infrastructure.mongoDB.model.runner_race_data_entity_property import RunnerRaceDataEntityProperty
from app.infrastructure.repository.repository_utils import load_repository_from_config


class RaceInfoService():

    def __init__(self):
        self.__downloader_runners_service = DownloaderRunnersService(HTTPDownloaderService(), MappeRunnersFactory(), RaceDownloaderOptionsFactory())
        db = load_repository_from_config()
        self.__race_info_repository = db.get_repository('race_info', RaceInfoEntity)
        self.__race_data_repository = db.get_repository('race_data', RaceDataEntity)

    # RAW
    def get_all_raw(self) -> List[RaceInfoRawModel]:
        all_race_info_entity: List[RaceInfoEntity] = self.__race_info_repository.get_all()
        all_race_data_entity: List[RaceDataEntity] = self.__race_data_repository.get_all()

        all_race_info_model: List[RaceInfoRawModel] = []

        for race_info_entity in all_race_info_entity:
            race_info_model = race_info_entity.to_domain_model(RaceInfoRawModel)

            if race_info_entity.race_data_id != '':
                for race_data_entity in all_race_data_entity:
                    if race_info_entity.race_data_id == race_data_entity.id:
                        data = race_data_entity.to_domain_model(RaceDataModel)
                        race_info_model.data = data

            all_race_info_model.append(race_info_model)

        return all_race_info_model

    def get_raw_by_id(self, race_id: str) -> RaceInfoRawModel:
        race_info_entity: RaceInfoEntity = self.__race_info_repository.get_by_id(race_id)

        if race_info_entity.race_data_id == '':
            return None

        race_data_entity: RaceDataEntity = self.__race_data_repository.get_by_id(race_info_entity.race_data_id)

        if race_data_entity is None:
            return None

        race_info_model:RaceInfoRawModel = race_info_entity.to_domain_model(RaceInfoRawModel)

        race_info_model.data = race_data_entity.to_domain_model(RaceDataModel)

        return race_info_model

    # Simplified
    def get_all_simplified(self) -> List[RaceInfoModel]:
        all_race_info_entity: List[RaceInfoEntity] = self.__race_info_repository.get_all()
        all_race_info_model = [race_info_entity.to_domain_model(RaceInfoModel) for race_info_entity in all_race_info_entity]

        return all_race_info_model

    def get_simplified_by_id(self, race_id) -> RaceInfoModel:
        result:RaceInfoEntity = self.__race_info_repository.get_by_id(race_id)
        return result.to_domain_model(RaceInfoModel)

    def add_simplified(self, race_model: RaceInfoModel) -> RaceInfoModel:
        new_race_entity = RaceInfoEntity().create_by_domain_model(race_model)

        race_id = self.__race_info_repository.add(new_race_entity)

        race:RaceInfoEntity = self.__race_info_repository.get_by_id(race_id)

        return race.to_domain_model(RaceInfoModel)

    # Common
    def process(self, race_id:str) -> RaceInfoModel:
        race_info_entity:RaceInfoEntity = self.__race_info_repository.get_by_id(race_id)

        race_info_model: RaceInfoModel = race_info_entity.to_domain_model(RaceInfoModel)

        if race_info_entity.race_data_id != '':
            self.__race_data_repository.delete_by_id(race_info_entity.race_data_id)

        runners_race_data_model:List[RunnerRaceDataModel] = self.__downloader_runners_service.get_all_runners(race_info_model)

        new_race_data_entity = RaceDataEntity()
        new_race_data_entity.data = [RunnerRaceDataEntityProperty().create_by_domain_model(runner_race_data_model) for runner_race_data_model in runners_race_data_model]

        new_race_data_id = self.__race_data_repository.add(new_race_data_entity)

        race_info_entity.race_data_id = new_race_data_id
        race_info_entity.processed = True

        status = self.__race_info_repository.update_by_id(race_info_entity.id, race_info_entity)
        race_info_entity = self.__race_info_repository.get_by_id(race_info_entity.id)

        return race_info_entity.to_domain_model(RaceInfoModel)

    def update_by_id(self, race_id:str, race_model:RaceInfoModel):
        new_race_entity = race_model.to_entity(RaceInfoEntity)

        status = self.__race_info_repository.update_by_id(race_id, new_race_entity)

        if status:
            race = self.__race_info_repository.get_by_id(race_id)
            return race
        else:
            return None

    def delete_by_id(self, race_id):
        status = self.__race_info_repository.delete_by_id(race_id)

        if status:
            return status

        return None
