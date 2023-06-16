"""
    TODO
"""
import logging
from app.infrastructure.mongoDB.person_list import PersonList
from app.model.person_model import PersonModel


class PersonController:
    """_summary_
    """
    def __init__(self, runner_repository:PersonList):
        self.runner_repository = runner_repository
        self.logger = logging.getLogger(__name__)

    def get_all(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        try:
            return self.runner_repository.get_all()
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
            return self.runner_repository.get_by_id(race_id)
        except Exception as exception_error: # pylint: disable=broad-except
            self.logger.error("Error retrieving race: %s", exception_error)
            return {'message': 'An error occurred while retrieving race.'}

    def add(self, new_runner: PersonModel):
        """_summary_

        Args:
            new_race (PersonModel): _description_

        Returns:
            _type_: _description_
        """
        try:
            self.runner_repository.add(new_runner)
            return {'message': 'La carrera se ha añadido correctamente.'}
        except Exception as exception_error: # pylint: disable=broad-except
            self.logger.error("Error adding race: %s", exception_error)
            return {'message': 'An error occurred while adding the race.'}

    def update_runner(self, runner_id: str, new_runner: PersonModel):
        """_summary_

        Args:
            race_id (str): _description_
            race (PersonModel): _description_

        Returns:
            _type_: _description_
        """
        try:
            result = self.runner_repository.update_by_id(runner_id, new_runner)

            if result.modified_count:
                return result
            else:
                return {'message': 'No se encontró la carrera especificada.'}
        except Exception as exception_error: # pylint: disable=broad-except
            self.logger.error("Error adding race: %s", exception_error)
            return {'message': 'An error occurred while adding the race.'}

    def delete_runner(self, runner_id: str):
        """_summary_

        Args:
            runner_id (str): _description_

        Returns:
            _type_: _description_
        """
        result = self.runner_repository.delete_by_id(runner_id)

        if result.deleted_count:
            return {'message': 'Carrera eliminada correctamente.'}

        return {'message': 'No se encontró la Carrera especificada.'}
