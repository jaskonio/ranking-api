import logging
from typing import Dict, List
from app.aplication.base_service import BaseService
from app.domain.model.league_model import League, LeagueRace, LeagueModel, ParticipantLeagueModel, RankingLeagueModel
from app.infrastructure.mongoDB.repository.ranking_league_repository import RankingLeagueRepository


class LeagueService(BaseService):
    def __init__(self, league_repository, ranking_league_repository:RankingLeagueRepository) -> None:
        super().__init__(league_repository)
        self.logger = logging.getLogger(__name__)
        self.__ranking_league_repository = ranking_league_repository

    def run_process(self, league_id:str) -> LeagueModel:
        league_raw_model:LeagueModel = self.get_raw_by_id(league_id)
        league_model = self.get_by_id(league_id)

        race_league_raw_models:List[LeagueRace] = list(sorted(league_raw_model.races, key=lambda x: x.order))

        for history_ranking in league_raw_model.history_ranking:
            self.__ranking_league_repository.delete_by_id(history_ranking.id)

        rankings = self.build_rankings(race_league_raw_models, league_raw_model.runner_participants)

        league_raw_model.history_ranking = []
        history_ranking_ids = []

        for race_id in rankings:
            for race_league in race_league_raw_models:
                if race_id == race_league.race_info.id:
                    ranking_league_model = RankingLeagueModel()
                    ranking_league_model.order = race_league.order
                    ranking_league_model.data = rankings[race_id]
                    ranking_result:RankingLeagueModel = self.__ranking_league_repository.add(ranking_league_model)
                    history_ranking_ids.append(ranking_result.id)

        if len(league_raw_model.history_ranking) != 0:
            league_raw_model.ranking_latest = league_raw_model.history_ranking[-1]

        league_model.history_ranking_ids = history_ranking_ids

        if len(history_ranking_ids) != 0:
            league_model.ranking_id = history_ranking_ids[-1]

        self.update_by_id(league_id, league_model)

        return self.get_raw_by_id(league_id)

    def build_rankings(self, race_league_raw_models:List[LeagueRace], runner_participants:List[ParticipantLeagueModel]):
        league_updated = League()
        
        for race_league_raw_model in race_league_raw_models:
            runners_in_league = []
            for runner in race_league_raw_model.runners:
                for runner_participant in runner_participants:
                    if runner.finished and runner.dorsal == runner_participant.dorsal:
                        runner.id = runner_participant.id
                        runner.photo_url = '' if runner_participant.photo_url is None else runner_participant.photo_url
                        runners_in_league.append(runner)
            league_updated.add_race(race_league_raw_model.race_info.id, runners_in_league)
        
        rankings:Dict[str, List[ParticipantLeagueModel]] = {}
    
        for race_id in league_updated.races:
            runners_list = league_updated.races[race_id]
            rankings[race_id] = runners_list

        return rankings