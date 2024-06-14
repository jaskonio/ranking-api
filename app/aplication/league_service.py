import logging
from typing import Dict, List
from app.aplication.base_service import BaseService
from app.domain.model.league_model import League, LeagueRace, LeagueModel, LeagueRanking, ParticipantLeagueModel, RankingLeagueModel
from app.domain.model.race_data_model import RaceDataModel
from app.infrastructure.mongoDB.repository.race_data_repository import RaceDataRepository
from app.infrastructure.mongoDB.repository.ranking_league_repository import RankingLeagueRepository


class LeagueService(BaseService):
    def __init__(self, league_repository, ranking_league_repository:RankingLeagueRepository, race_data_repository:RaceDataRepository) -> None:
        super().__init__(league_repository)
        self.logger = logging.getLogger(__name__)
        self.__ranking_league_repository = ranking_league_repository
        self.__race_data_repository = race_data_repository

    def run_process(self, league_id:str) -> LeagueModel:
        league_model:LeagueModel = self.get_by_id(league_id)

        for history_rankings in league_model.history_ranking:
            self.__ranking_league_repository.delete_by_id(history_rankings.id)

        rankings = self.__build_rankings(league_model.races ,league_model.runner_participants)

        league_model.history_ranking = []

        history_ranking:List[LeagueRanking]= []

        for race_id in rankings:
            for race_league in league_model.races:
                if race_id == race_league.id:
                    ranking_league = LeagueRanking()
                    ranking_league.order = race_league.order
                    ranking_league.data = rankings[race_id]
                    ranking_league.id = race_id
                    history_ranking.append(ranking_league)

        if len(league_model.history_ranking) != 0:
            league_model.ranking_latest = league_model.history_ranking[-1]

        self.update_by_id(league_id, league_model)

        return self.get_raw_by_id(league_id)

    def __build_rankings(self, races:List[LeagueRace], runner_participants:List[ParticipantLeagueModel]):
        league_updated = League()
        
        all_race_data:List[RaceDataModel] = self.__race_data_repository.get_all_raw()
    
        for race in races:
            for race_data in all_race_data:
                if race.race_data_id == race_data.id:
                    runners_in_league = []
                    for data_runner in race_data.runners:
                        for runner_participant in runner_participants:
                            if data_runner.finished and data_runner.dorsal == runner_participant.dorsal:
                                runners_in_league.append(data_runner)
                    league_updated.add_race(race.id, runners_in_league)
        
        rankings:Dict[str, List[ParticipantLeagueModel]] = {}
    
        for race_id in league_updated.races:
            runners_list = league_updated.races[race_id]
            rankings[race_id] = runners_list

        return rankings