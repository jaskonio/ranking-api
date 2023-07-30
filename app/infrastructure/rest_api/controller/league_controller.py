import logging
from typing import List
from app.aplication.league_service import LeagueService
from app.domain.model.league import League
from app.domain.model.runner import Runner


class LeagueController():
    def __init__(self, league_service:LeagueService):
        self.__league_service = league_service
        self.logger = logging.getLogger(__name__)

    def get_all(self):
        try:
            return self.__league_service.get_all()
        except Exception as exception_error:
            self.logger.error("Error retrieving all items: %s", exception_error)
            raise TypeError('An error occurred while retrieving all items.') from None

    def get_by_id(self, league_id):
        try:
            league = self.__league_service.get_by_id(league_id)

            if league:
                return league

            return {}
        except Exception as exception_error:
            self.logger.error("Error retrieving item: %s", exception_error)
            raise TypeError('An error occurred while retrieving item.') from None

    def add(self, league: League):
        try:
            league = self.__league_service.add(league)

            if league:
                return league

            return {}
        except Exception as exception_error:
            self.logger.error("Error saving: %s", exception_error)
            raise TypeError('An error occurred while saving.') from None

    def add_runners(self, league_id:str, new_runners:List[Runner]):
        try:
            league = self.__league_service.add_runners(league_id, new_runners)

            if league:
                return league

            return {}
        except Exception as exception_error:
            self.logger.error("Error saving: %s", exception_error)
            raise TypeError('An error occurred while saving.') from None

    def add_runner(self, league_id:str, new_runner:Runner):
        try:
            league = self.__league_service.add_runner(league_id, new_runner)

            if league:
                return league

            return {}
        except Exception as exception_error:
            self.logger.error("Error saving: %s", exception_error)
            raise TypeError('An error occurred while saving.') from None

    def delete_runners(self, league_id:str, runners:List[Runner]):
        try:
            league = self.__league_service.delete_runners(league_id, runners)

            if league:
                return league

            return {}
        except Exception as exception_error:
            self.logger.error("Error saving: %s", exception_error)
            raise TypeError('An error occurred while saving.') from None

    def delete_runner(self, league_id:str, runner:Runner):
        try:
            league = self.__league_service.delete_runner(league_id, runner)

            if league:
                return league

            return {}
        except Exception as exception_error:
            self.logger.error("Error saving: %s", exception_error)
            raise TypeError('An error occurred while saving.') from None

    def add_race(self, league_id, race_id:str, order_race:int):
        try:
            league = self.__league_service.add_race(league_id, race_id, order_race)

            if league:
                return league

            return {}
        except Exception as exception_error:
            self.logger.error("Error saving: %s", exception_error)
            raise TypeError('An error occurred while saving.') from None

    def disqualify_runner(self, league_id:int, race_name:str, bib_number):
        try:
            league = self.__league_service.disqualify_runner(league_id, race_name, bib_number)

            if league:
                return league

            return {}
        except Exception as exception_error:
            self.logger.error("Error saving: %s", exception_error)
            raise TypeError('An error occurred while saving.') from None

    def update_by_id(self, league_id:str, new_league: League):
        try:
            league = self.__league_service.update_by_id(league_id, new_league)

            if league:
                return league

            return {}
        except Exception as exception_error:
            self.logger.error("Error updating: %s", exception_error)
            raise TypeError('An error occurred while updating.') from None

    def delete_by_id(self, league_id):
        try:
            status = self.__league_service.delete_by_id(league_id)

            if status:
                return status

            return {}
        except Exception as exception_error:
            self.logger.error("Error deleting: %s", exception_error)
            raise TypeError('An error occurred while deleting.') from None
