"""
    TODO
"""
import logging
from typing import List
from app.domain.DownloaderService import DownloaderService
from app.infrastructure.mongoDB.RaceList import RaceList
from app.model.RaceBaseModel import RaceBaseModel
from app.model.RunnerModel import RunnerModel

class RaceController:
    """_summary_
    """
    def __init__(self, race_repository:RaceList, downloader_service:DownloaderService):
        self.race_repository = race_repository
        self.downloader_service = downloader_service
        self.logger = logging.getLogger(__name__)

    def get_all(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        try:
            return self.race_repository.get_all()
        except Exception as exception_error: # pylint: disable=broad-except
            self.logger.error("Error retrieving all races: %s", exception_error)
            return {'message': 'An error occurred while retrieving all races.'}

    def get_by_id(self, race_id:str):
        """_summary_

        Args:
            race_id (str): _description_

        Returns:
            _type_: _description_
        """
        try:
            return self.race_repository.get_by_id(race_id)
        except Exception as exception_error: # pylint: disable=broad-except
            self.logger.error("Error retrieving race: %s", exception_error)
            return {'message': 'An error occurred while retrieving race.'}

    def add_race(self, new_race: RaceBaseModel):
        """_summary_

        Args:
            new_race (RaceBaseModel): _description_

        Returns:
            _type_: _description_
        """
        try:
            if new_race.proceesEnabled:
                runners:List[RunnerModel] = self.downloader_service.download_race_data(new_race.url)
                new_race.set_ranking(runners)

            self.race_repository.add_race(new_race)

            return {'message': 'La carrera se ha añadido correctamente.'}
        except Exception as exception_error: # pylint: disable=broad-except
            self.logger.error("Error adding race: %s", exception_error)
            return {'message': 'An error occurred while adding the race.'}

    def update_race(self, race_id: str, race: RaceBaseModel):
        """_summary_

        Args:
            race_id (str): _description_
            race (RaceBaseModel): _description_

        Returns:
            _type_: _description_
        """
        try:
            if race.proceesEnabled:
                runners:List[RunnerModel] = self.downloader_service.download_race_data(race.url)
                race.set_ranking(runners)

            result = self.race_repository.update_race(race_id, race)

            if result.modified_count:
                return race
            else:
                return {'message': 'No se encontró la carrera especificada.'}
        except Exception as exception_error: # pylint: disable=broad-except
            self.logger.error("Error adding race: %s", exception_error)
            return {'message': 'An error occurred while adding the race.'}

    def delete_race(self, race_id: str):
        """_summary_

        Args:
            race_id (str): _description_

        Returns:
            _type_: _description_
        """
        result = self.race_repository.delete_race(race_id)

        if result.deleted_count:
            return {'message': 'Carrera eliminada correctamente.'}

        return {'message': 'No se encontró la Carrera especificada.'}
