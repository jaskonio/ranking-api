import logging
from typing import Dict, List
from app.aplication.base_service import BaseService
from app.domain.model.league_model import League, LeagueRace, LeagueModel, LeagueRankingModel, ParticipantLeagueModel
from app.domain.model.race_data_model import RaceDataModel, RunnerRaceDataModel
from app.infrastructure.mongoDB.repository.race_data_repository import RaceDataRepository


class LeagueService(BaseService):
    def __init__(self, league_repository, race_data_repository:RaceDataRepository) -> None:
        super().__init__(league_repository)
        self.logger = logging.getLogger(__name__)
        self.__race_data_repository = race_data_repository

    def run_process(self, league_id:str) -> LeagueModel:
        """
        Ejecuta el proceso de actualización de rankings para una liga específica.
        """
        league_model:LeagueModel = self.get_by_id(league_id)
        rankings = self.__build_rankings(league_model.races ,league_model.runner_participants)

        league_model.history_ranking = [
            LeagueRankingModel(order=race_league.order, data=rankings[race_league.id])
            for race_league in league_model.races if race_league.id in rankings
        ]

        if len(league_model.history_ranking) != 0:
            league_model.ranking_latest = league_model.history_ranking[-1]

        self.update_by_id(league_id, league_model)

        return self.get_by_id(league_id)

    def __build_rankings(self, races:List[LeagueRace], runner_participants:List[ParticipantLeagueModel]):
        """
        Construye los rankings para las carreras de una liga.
        """
        league  = League()
        all_race_data:List[RaceDataModel] = self.__race_data_repository.get_all()
        runner_map = {runner.person_id: runner for runner in runner_participants}
    
        for race in races:
            race_runners = self._get_race_runners(race, all_race_data, runner_map)
            race_runners_filtered:List[RunnerRaceDataModel] = []
            for race_runner in race_runners:
                for runner_participant in runner_participants:
                    if race_runner.first_name.lower() == runner_participant.first_name.lower() and race_runner.last_name.lower() == runner_participant.last_name.lower():
                        race_runners_filtered.append(race_runner)

            league.add_race(race.id, race_runners_filtered)

        return {race_id: league.races[race_id] for race_id in league.races}

    def _get_race_runners(self, race: LeagueRace, all_race_data: List[RaceDataModel], runner_map: Dict[str, ParticipantLeagueModel]) -> List[RunnerRaceDataModel]:
        """
        Obtiene los corredores correspondientes a una carrera específica.
        """
        for race_data in all_race_data:
            if race.race_data_id == race_data.id:
                return [ self._match_runner(data_runner, runner_map) for data_runner in race_data.runners if data_runner.finished]
        return []

    def _match_runner(self, data_runner: RunnerRaceDataModel, runner_map: Dict[str, ParticipantLeagueModel]) -> RunnerRaceDataModel:
        """
        Encuentra el participante correspondiente al corredor en los datos de la carrera.
        """
        for runner_participant in runner_map.values():
            if runner_participant.unique_dorsal and data_runner.dorsal == runner_participant.dorsal:
                data_runner.id = runner_participant.id
                data_runner.person_id = runner_participant.person_id
                return data_runner
            if not runner_participant.unique_dorsal and runner_participant.first_name.lower() == data_runner.first_name.lower() and runner_participant.last_name.lower() == data_runner.last_name.lower():
                data_runner.id = runner_participant.id
                data_runner.person_id = runner_participant.person_id
                return data_runner
        return data_runner