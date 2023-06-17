"""
    TODO
"""
import logging
from app.infrastructure.mongoDB.base_list import BaseList
from app.model.BaseMongoModel import BaseMongoModel

class BaseController:
    """_summary_
    """
    def __init__(self, repository:BaseList):
        self.repository = repository
        self.logger = logging.getLogger(__name__)

    def get_all(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        try:
            return self.repository.get_all()
        except Exception as exception_error: # pylint: disable=broad-except
            self.logger.error("Error retrieving all items: %s", exception_error)
            raise TypeError('An error occurred while retrieving all items.') from None

    def get_by_id(self, race_id:str):
        """_summary_

        Args:
            race_id (str): _description_

        Returns:
            _type_: _description_
        """
        try:
            return self.repository.get_by_id(race_id)
        except Exception as exception_error: # pylint: disable=broad-except
            self.logger.error("Error retrieving race: %s", exception_error)
            return {'message': 'An error occurred while retrieving race.'}

    def add(self, new_runner: BaseMongoModel):
        """_summary_

        Args:
            new_race (BaseMongoModel): _description_

        Returns:
            _type_: _description_
        """
        try:
            result = self.repository.add(new_runner)
            return result
        except Exception as exception_error: # pylint: disable=broad-except
            self.logger.error("Error adding race: %s", exception_error)
            return {'message': 'An error occurred while adding the race.'}

    def update_by_id(self, runner_id: str, new_runner: BaseMongoModel):
        """_summary_

        Args:
            race_id (str): _description_
            race (BaseMongoModel): _description_

        Returns:
            _type_: _description_
        """
        try:
            result = self.repository.update_by_id(runner_id, new_runner)

            if result.modified_count:
                return result
            else:
                return {'message': 'No se encontró la carrera especificada.'}
        except Exception as exception_error: # pylint: disable=broad-except
            self.logger.error("Error adding race: %s", exception_error)
            return {'message': 'An error occurred while adding the race.'}

    def delete_by_id(self, runner_id: str):
        """_summary_

        Args:
            runner_id (str): _description_

        Returns:
            _type_: _description_
        """
        result = self.repository.delete_by_id(runner_id)

        if result.deleted_count:
            return {'message': 'Carrera eliminada correctamente.'}

        return {'message': 'No se encontró la Carrera especificada.'}
