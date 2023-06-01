import logging
from typing import List
from app.domain.DownloaderService import DownloaderService
from app.infrastructure.mongoDB.RaceList import RaceList
from app.model.RaceBaseModel import RaceBaseModel
from app.model.RunnerModel import RunnerModel

class RaceController:
    def __init__(self, race_repository:RaceList, downloader_service:DownloaderService):
        self.race_repository = race_repository
        self.downloader_service = downloader_service
        self.logger = logging.getLogger(__name__)

    def get_all(self):
        try:
            return self.race_repository.get_all()
        except Exception as e:
            self.logger.error(f"Error retrieving all races: {str(e)}")
            return {'message': 'An error occurred while retrieving all races.'}

    def get_by_id(self, race_id:str):
        try:
            return self.race_repository.get_by_id(race_id)
        except Exception as e:
            self.logger.error(f"Error retrieving race: {str(e)}")
            return {'message': 'An error occurred while retrieving race.'}

    def add_race(self, new_race: RaceBaseModel):
        try:
            if new_race.proceesEnabled:
                runners:List[RunnerModel] = self.downloader_service.download_race_data(new_race.url)
                new_race.set_ranking(runners)

            self.race_repository.add_race(new_race)

            return {'message': 'La carrera se ha añadido correctamente.'}
        except Exception as e:
            self.logger.error(f"Error adding race: {str(e)}")
            return {'message': 'An error occurred while adding the race.'}

    def update_race(self, race_id: str, race: RaceBaseModel):
        try:
            if race.proceesEnabled:
                runners:List[RunnerModel] = self.downloader_service.download_race_data(race.url)
                race.set_ranking(runners)

            result = self.race_repository.update_race(race_id, race)

            if result.modified_count:
                return race
            else:
                return {'message': 'No se encontró la carrera especificada.'}
        except Exception as e:
            self.logger.error(f"Error adding race: {str(e)}")
            return {'message': 'An error occurred while adding the race.'}

    def delete_race(self, race_id: str):
        result = self.race_repository.delete_race(race_id)

        if result.deleted_count:
            return {'message': 'Carrera eliminada correctamente.'}
        else:
            return {'message': 'No se encontró la Carrera especificada.'}
