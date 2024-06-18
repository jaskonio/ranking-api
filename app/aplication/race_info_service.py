from typing import List
from app.aplication.base_service import BaseService
from app.domain.model.race_data_model import RaceDataModel, RunnerRaceDataModel
from app.domain.model.race_info_model import RaceModel
from app.domain.repository.igeneric_repository import IGenericRepository
from app.domain.services.downloader_runners_service import DownloaderRunnersService
from app.infrastructure.mongoDB.repository.race_data_repository import RaceDataRepository


class RaceInfoService(BaseService):
    def __init__(self, repository:IGenericRepository,downloader_runners_service: DownloaderRunnersService, race_data_repository: RaceDataRepository):
        super().__init__(repository)
        self.__downloader_runners_service = downloader_runners_service
        self.__race_data_repository = race_data_repository

    def delete_by_id(self, model_id: str) -> bool:
        race_info_model:RaceModel = self.get_by_id(model_id)
        if race_info_model is None:
            return False

        self.repository.delete_by_id(model_id)

        if race_info_model.race_data_id is not None:
            self.__race_data_repository.delete_by_id(race_info_model.race_data_id)

        return True

    # Common
    def process(self, race_id:str) -> RaceModel:
        try:
            race_info_model: RaceModel = self.repository.get_by_id(race_id)

            runners_race_data_model:List[RunnerRaceDataModel] = self.__downloader_runners_service.get_all_runners(race_info_model)

            if race_info_model.race_data_id != '':
                self.__race_data_repository.delete_by_id(race_info_model.race_data_id)

            new_race_data_model = RaceDataModel()
            new_race_data_model.runners = runners_race_data_model

            new_race_data_model:RaceDataModel = self.__race_data_repository.add(new_race_data_model)

            race_info_model.race_data_id = str(new_race_data_model.id)
            race_info_model.processed = True

            race_info_model = self.repository.update_by_id(race_id, race_info_model)

            return race_info_model
        except Exception as exception_error:
            self.logger.error("Error process race. ", exception_error)
            return None
