import logging
from typing import List
from app.aplication.base_service import BaseService
from app.domain.model.league_model import League, LeagueModel, LeagueRAWModel
from app.domain.model.participant_ranking_model import ParticipantRankingModel
from app.domain.model.race_league_model import RaceLeagueRawModel
from app.domain.model.ranking_league_model import RankingLeagueModel
from app.infrastructure.mongoDB.repository.ranking_league_repository import RankingLeagueRepository


class LeagueService(BaseService):
    def __init__(self, league_repository, ranking_league_repository:RankingLeagueRepository) -> None:
        super().__init__(league_repository)
        self.logger = logging.getLogger(__name__)
        self.__ranking_league_repository = ranking_league_repository

    def run_process(self, league_id:str) -> LeagueRAWModel:
        league_raw_model:LeagueRAWModel = self.get_raw_by_id(league_id)
        race_league_raw_models:List[RaceLeagueRawModel] = list(sorted(league_raw_model.races, key=lambda x: x.order, reverse=True))

        for history_ranking in league_raw_model.history_ranking:
            self.__ranking_league_repository.delete_by_id(history_ranking.id)

        league_updated = League()
        
        for race_league_raw_model in race_league_raw_models:
            runners_in_league = []
            for runner in race_league_raw_model.runners:
                for runner_participant in league_raw_model.runner_participants:
                    if runner.dorsal == runner_participant.dorsal:
                        runner.id = runner_participant.id
                        runner.photo_url = runner_participant.photo_url
                        runners_in_league.append(runner)
            league_updated.add_race(runners_in_league)
        
        rankings_models = []
        for rankings in league_updated.rankings:
            ranking: List[ParticipantRankingModel]= []
            for runner_id in rankings:
                ranking.append(rankings[str(runner_id)])
            rankings_models.append(ranking)

        league_raw_model.history_ranking = []
        history_ranking_ids = []
        for index, rankings_model in enumerate(rankings_models):
            ranking_league_model = RankingLeagueModel()
            ranking_league_model.order = index
            ranking_league_model.data = rankings_model
            ranking_result:RankingLeagueModel = self.__ranking_league_repository.add(ranking_league_model)
            history_ranking_ids.append(ranking_result.id)

        if len(league_raw_model.history_ranking) != 0:
            league_raw_model.ranking_latest = league_raw_model.history_ranking[-1]
        
        league_model:LeagueModel = self.get_by_id(league_id)
        league_model.history_ranking_ids = history_ranking_ids
        if len(history_ranking_ids) != 0:
            league_model.ranking_id = history_ranking_ids[-1]

        self.update_by_id(league_id, league_model)

        return self.get_raw_by_id(league_id)
