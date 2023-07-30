"""
    TODO
"""
import logging
from typing import List
from app.infrastructure.mongoDB.LeagueList import LeagueList
from app.infrastructure.mongoDB.person_list import PersonList
from app.model.league_model import LeagueModel
from app.model.person_model import PersonModel


class PersonController():
    """_summary_
    """
    def __init__(self, runner_repository:PersonList, league_repository:LeagueList):
        self.__repository = runner_repository
        self.__league_repository = league_repository
        self.logger = logging.getLogger(__name__)

    def get_all(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        try:
            return self.__repository.get_all()
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
            return self.__repository.get_by_id(race_id)
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
            result = self.__repository.add(new_runner)
            return result
        except Exception as exception_error: # pylint: disable=broad-except
            self.logger.error("Error adding race: %s", exception_error)
            return {'message': 'An error occurred while adding the race.'}

    def update_by_id(self, runner_id: str, new_runner: PersonModel):
        """_summary_

        Args:
            race_id (str): _description_
            race (PersonModel): _description_

        Returns:
            _type_: _description_
        """
        try:
            result = self.__repository.update_by_id(runner_id, new_runner)

            if result.modified_count:
                leagues:List[LeagueModel] = self.__league_repository.get_all()

                for league in leagues:
                    for runner_participant in league.runnerParticipants:
                        if runner_participant.name + ' ' + runner_participant.last_name == new_runner.first_name + ' ' + new_runner.last_name:
                            runner_participant.photo = new_runner.photo
                            self.__league_repository.update_league(league.id, league)
                            break

                return {'message': 'El item se ha actualizado correctamente.'}
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
        result = self.__repository.delete_by_id(runner_id)

        if result.deleted_count:
            return {'message': 'El Item se ha eliminado correctamente.'}

        return {'message': 'No se encontró el Item especificada.'}
