from typing import List
from app.aplication.base_service import BaseService
from app.aplication.person_service import PersonService
from app.domain.model.race_data_model import RaceDataRawModel
from app.domain.model.race_info_model import RaceInfoRawModel, RaceInfoModel
from app.domain.model.runner_race_data_model import RunnerRaceDataModel
from app.domain.repository.igeneric_repository import IGenericRepository
from app.domain.services.downloader_runners_service import DownloaderRunnersService
from app.infrastructure.mongoDB.model.club_info_entity import ClubInfoEntity
from app.infrastructure.mongoDB.model.race_data_entity import RaceDataEntity
from app.infrastructure.mongoDB.model.race_info_entity import RaceInfoEntity
from app.infrastructure.mongoDB.model.runner_race_data_entity import RunnerRaceDataEntity


class RaceInfoService(BaseService):

    def __init__(self, repository:IGenericRepository, model_type:RaceInfoModel, entity_type:RaceInfoEntity
                 , downloader_runners_service: DownloaderRunnersService, race_data_repository: IGenericRepository, club_info_repository: IGenericRepository
                 , runner_race_data_repository: IGenericRepository, person_service: PersonService):
        super().__init__(repository, model_type, entity_type)

        self.__downloader_runners_service = downloader_runners_service
        self.__race_data_repository = race_data_repository
        self.__club_info_repository = club_info_repository
        self.__runner_race_data_repository = runner_race_data_repository
        self.__person_service = person_service

    def get_all_raw(self) -> List[RaceInfoRawModel]:
        all_race_info_entities:List[RaceInfoEntity] = self.__repository.get_all()
        all_race_data_entities:List[RaceDataEntity] = self.__race_data_repository.get_all()
        all_runner_race_data_entities:List[RunnerRaceDataEntity] = self.__runner_race_data_repository.get_all()

        all_race_info_model: List[RaceInfoRawModel] = []

        for race_info_entity in all_race_info_entities:
            race_info_model:RaceInfoRawModel = race_info_entity.to_domain_model(RaceInfoRawModel)

            for race_data_entity in all_race_data_entities:
                if race_info_entity.race_data_id == race_data_entity.id:
                    race_data_model:RaceDataRawModel  = race_data_entity.to_domain_model(RaceDataRawModel)

                    for runner_id in race_data_entity.runner_ids:
                        for runner_race_data_entity in all_runner_race_data_entities:
                            if runner_id in runner_race_data_entity.id:
                                race_data_model.runners.append(runner_race_data_entity.to_domain_model(RunnerRaceDataModel))

                    race_info_model.race_data = race_data_model

            all_race_info_model.append(race_info_model)

        return all_race_info_model

    def get_raw_by_id(self, race_id: str) -> RaceInfoRawModel:
        race_info_entity:RaceInfoEntity = self.__repository.get_by_id(race_id)

        if race_info_entity.race_data_id == '':
            return None

        race_data_entity: RaceDataEntity = self.__race_data_repository.get_by_id(race_info_entity.race_data_id)

        if race_data_entity is None:
            return None

        runner_race_data_models: List[RunnerRaceDataModel] = []

        for runner_id in race_data_entity.runner_ids:
            runner_race_data_entity:RunnerRaceDataEntity = self.__runner_race_data_repository.get_by_id(runner_id)
            runner_race_data_model:RunnerRaceDataModel = runner_race_data_entity.to_domain_model(RunnerRaceDataModel)
            runner_race_data_models.append(runner_race_data_model)

        race_data_model:RaceDataRawModel = race_data_entity.to_domain_model(RaceDataRawModel)
        race_data_model.runners = runner_race_data_models

        race_info_model:RaceInfoRawModel = race_info_entity.to_domain_model(RaceInfoRawModel)

        race_info_model.race_data = race_data_model

        return race_info_model

    # Common
    def process(self, race_id:str) -> RaceInfoModel:
        race_info_entity:RaceInfoEntity = self.__repository.get_by_id(race_id)

        race_info_model: RaceInfoModel = race_info_entity.to_domain_model(RaceInfoModel)

        if race_info_entity.race_data_id != '':
            self.__race_data_repository.delete_by_id(race_info_entity.race_data_id)

        runners_race_data_model:List[RunnerRaceDataModel] = self.__downloader_runners_service.get_all_runners(race_info_model)

        # Filter by club and person
        club_info_entity:ClubInfoEntity =self.__club_info_repository.get_all()[0]
        person_models = self.__person_service.get_all()

        new_race_data_entity = RaceDataEntity()

        for runner_model in runners_race_data_model:
            if runner_model.club.lower() in club_info_entity.names:
                for person_model in person_models:
                    if person_model == runner_model:
                        runner_model.person_id = person_model.id
                        runner_model.last_name = person_model.last_name
                        runner_model.first_name = person_model.first_name
                        runner_model.gender = person_model.gender
                        runner_model.photo_url = person_model.photo_url

                        runner_entity_id = self.__runner_race_data_repository.add(RunnerRaceDataEntity().create_by_domain_model(runner_model))
                        new_race_data_entity.runner_ids.append(runner_entity_id)

        new_race_data_id = self.__race_data_repository.add(new_race_data_entity)

        race_info_entity.race_data_id = new_race_data_id
        race_info_entity.processed = True

        race_info_entity = self.__repository.update_by_id(race_info_entity.id, race_info_entity)

        return race_info_entity.to_domain_model(RaceInfoModel)
