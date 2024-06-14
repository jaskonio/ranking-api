import logging
from typing import Dict, List
from app.aplication.base_service import BaseService
from app.domain.model.league_model import League, LeagueRace, LeagueModel, LeagueRankingModel, ParticipantLeagueModel
from app.domain.model.race_data_model import RaceDataModel
from app.infrastructure.mongoDB.repository.race_data_repository import RaceDataRepository


class LeagueService(BaseService):
    def __init__(self, league_repository, race_data_repository:RaceDataRepository) -> None:
        super().__init__(league_repository)
        self.logger = logging.getLogger(__name__)
        self.__race_data_repository = race_data_repository

    def run_process(self, league_id:str) -> LeagueModel:
        league_model:LeagueModel = self.get_by_id(league_id)

        rankings = self.__build_rankings(league_model.races ,league_model.runner_participants)

        league_model.history_ranking = []

        for race_id in rankings:
            for race_league in league_model.races:
                if race_id == race_league.id:
                    ranking_league = LeagueRankingModel()
                    ranking_league.order = race_league.order
                    ranking_league.data = rankings[race_id]
                    league_model.history_ranking.append(ranking_league)

        if len(league_model.history_ranking) != 0:
            league_model.ranking_latest = league_model.history_ranking[-1]

        result = self.update_by_id(league_id, league_model)

        return self.get_by_id(league_id)

    def __build_rankings(self, races:List[LeagueRace], runner_participants:List[ParticipantLeagueModel]):
        league_updated = League()
        
        all_race_data:List[RaceDataModel] = self.__race_data_repository.get_all()
    
        for race in races:
            for race_data in all_race_data:
                if race.race_data_id == race_data.id:
                    runners_in_league = []
                    for data_runner in race_data.runners:
                        for runner_participant in runner_participants:
                            if data_runner.finished:
                                if runner_participant.unique_dorsal:
                                    if data_runner.dorsal == runner_participant.dorsal:
                                        data_runner.person_id = runner_participant.person_id
                                        runners_in_league.append(data_runner)
                                else:
                                    if runner_participant.first_name.lower() == data_runner.first_name.lower() and runner_participant.last_name.lower() == data_runner.last_name.lower():
                                        data_runner.person_id = runner_participant.person_id
                                        runners_in_league.append(data_runner) 

                    league_updated.add_race(race.id, runners_in_league)
        
        rankings:Dict[str, List[ParticipantLeagueModel]] = {}
    
        for race_id in league_updated.races:
            runners_list = league_updated.races[race_id]
            rankings[race_id] = runners_list

        return rankings