from typing import List
from app.aplication.base_service import BaseService
from app.domain.model.club_info_model import ClubInfoModel
from app.domain.model.person_model import PersonModel
from app.domain.model.race_data_model import RaceDataModel
from app.domain.model.race_info_model import RaceInfoModel
from app.domain.model.runner_race_data_model import RunnerRaceDataModel
from app.domain.repository.igeneric_repository import IGenericRepository
from app.domain.services.downloader_runners_service import DownloaderRunnersService


class RaceInfoService(BaseService):
    def __init__(self, repository:IGenericRepository,downloader_runners_service: DownloaderRunnersService, race_data_repository: IGenericRepository
                 , club_info_repository: IGenericRepository, runner_race_data_repository: IGenericRepository, __person_repository:IGenericRepository):
        super().__init__(repository)
        self.__downloader_runners_service = downloader_runners_service
        self.__race_data_repository = race_data_repository
        self.__club_info_repository = club_info_repository
        self.__runner_race_data_repository = runner_race_data_repository
        self.__person_repository = __person_repository

    # Common
    def process(self, race_id:str) -> RaceInfoModel:
        race_info_model: RaceInfoModel = self.repository.get_by_id(race_id)

        if race_info_model.race_data_id != '':
            self.__race_data_repository.delete_by_id(race_info_model.race_data_id)

        runners_race_data_model:List[RunnerRaceDataModel] = self.__downloader_runners_service.get_all_runners(race_info_model)

        # Filter by club and person
        club_info_model:ClubInfoModel =self.__club_info_repository.get_all()
        club_info_model_names = []
    
        if len(club_info_model) == 0:
            raise TypeError("Falta informacion del club")
        else:
            club_info_model = club_info_model[0]
            club_info_model_names = [name.lower() for name in club_info_model.names]

        person_models:List[PersonModel] = self.__person_repository.get_all()

        new_race_data_model = RaceDataModel()

        for runner_model in runners_race_data_model:
            if runner_model.club.lower() in club_info_model_names:
                for person_model in person_models:
                    if person_model == runner_model:
                        runner_model.person_id = person_model.id
                        runner_model.last_name = person_model.last_name
                        runner_model.first_name = person_model.first_name
                        runner_model.gender = person_model.gender
                        runner_model.photo_url = person_model.photo_url

                        new_runner_race_data_model:RunnerRaceDataModel = self.__runner_race_data_repository.add(runner_model)
                        new_race_data_model.runner_ids.append(str(new_runner_race_data_model.id))

        new_race_data_model:RaceDataModel = self.__race_data_repository.add(new_race_data_model)

        race_info_model.race_data_id = str(new_race_data_model.id)
        race_info_model.processed = True

        race_info_model = self.repository.update_by_id(race_id, race_info_model)

        return race_info_model
