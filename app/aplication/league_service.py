import logging
from typing import List
from app.domain.model.league_model import LeagueModel
from app.domain.model.person_model import PersonModel
from app.domain.model.deprecated.race import Race
from app.domain.model.deprecated.race_base import RaceBase
from app.domain.model.deprecated.runner_base import RunnerBase
from app.domain.repository.igeneric_repository import IGenericRepository


class LeagueService():

    def __init__(self, league_repository:IGenericRepository
                 , race_repository:IGenericRepository
                 , person_repository:IGenericRepository) -> None:
        self.league_repository = league_repository
        self.race_repository = race_repository
        self.person_repository = person_repository
        self.logger = logging.getLogger(__name__)

    def get_all(self) -> List[LeagueModel]:
        leagues = self.league_repository.get_all()

        return leagues

    def get_by_id(self, league_id) -> LeagueModel:
        league = self.league_repository.get_by_id(league_id)

        return league

    def add(self, league) -> LeagueModel:
        league_id = self.league_repository.add(league)

        league = self.league_repository.get_by_id(league_id)

        return league

    def add_runners(self, league_id:str, runners:List[RunnerBase]):
        league:LeagueModel = self.league_repository.get_by_id(league_id)

        if league is None:
            self.logger.error("League not found.")
            return None

        league.add_runners(runners)

        self.league_repository.update_by_id(league_id, league)
        self.logger.info("Runner added successfully.")

        return league

    def add_runner(self, league_id:str, runner:RunnerBase):
        league:LeagueModel = self.league_repository.get_by_id(league_id)

        if league is None:
            self.logger.error("League not found.")
            return None

        person:RunnerBase = self.person_repository.get_by_id(runner.id)

        if person is None:
            self.logger.warn("Person not found. Id: " + str(runner.id))
            return None

        person.dorsal = runner.dorsal

        league.add_runner(person)

        self.league_repository.update_by_id(league_id, league)
        self.logger.info("Runner added successfully.")

        return league

    def delete_runners(self, league_id:str, runners:List[RunnerBase]):
        league:LeagueModel = self.league_repository.get_by_id(league_id)

        if league is None:
            self.logger.error("League not found.")
            return None

        league.delete_runners(runners)

        self.league_repository.update_by_id(league_id, league)
        self.logger.info("Runner added successfully.")

        return league

    def delete_runner(self, league_id:str, runner:RunnerBase):
        league:LeagueModel = self.league_repository.get_by_id(league_id)

        if league is None:
            self.logger.error("League not found.")
            return None

        league.delete_runner(runner)

        self.league_repository.update_by_id(league_id, league)
        self.logger.info("Runner added successfully.")

        return league

    def add_race(self, league_id, race_id:str, order_race:int):
        league:LeagueModel = self.league_repository.get_by_id(league_id)

        if league is None:
            self.logger.error("League not found.")
            return None

        race:RaceBase = self.race_repository.get_by_id(race_id)

        if race is None:
            self.logger.error("Race not found.")
            return None

        new_race = Race(id=0, name=race.name, url=race.url, ranking=race.ranking, order=order_race)

        league.add_race(new_race)
        self.league_repository.update_by_id(league_id, league)

        return league

    def disqualify_runner(self, league_id:int, race_name:str, bib_number):
        league:LeagueModel = self.league_repository.get_by_id(league_id)

        if league is None:
            self.logger.error("League not found.")
            return None

        if len(league.races) == 0:
            self.logger.error("No se encontró la carrera especificada.")
            return None

        league.disqualify_runner_process(bib_number, race_name)

        status = self.league_repository.update_by_id(league_id, league)

        if status:
            league = self.league_repository.get_by_id(league_id)
            return league
        else:
            return None

    def update_by_id(self, league_id:str, new_league:LeagueModel):
        league = LeagueModel()

        league.id = league_id
        league.name = new_league.name

        league.add_runners(new_league.participants)
        league.add_races(new_league.races)

        status = self.league_repository.update_by_id(league_id, league)

        if status:
            league = self.league_repository.get_by_id(league_id)
            return league

        return None

    def delete_by_id(self, league_id):
        status = self.league_repository.delete_by_id(league_id)

        if status:
            return status

        return None
