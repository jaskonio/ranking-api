from typing import List
from app.domain.model.league_model import LeagueModel, LeagueRaw, RankingLeagueModel
from app.domain.model.person_model import PersonModel
from app.domain.model.race_info_model import RaceInfoRawModel
from app.domain.repository.igeneric_repository import IGenericRepository
from app.infrastructure.mongoDB.model.league_entity import LeagueEntity
from app.infrastructure.mongoDB.repository.mongo_db_repository import MongoDBRepository
from app.infrastructure.mongoDB.repository.ranking_league_repository import RankingLeagueRepository


class LeagueRepository(MongoDBRepository):
    def __init__(self, race_info_repository:IGenericRepository, person_repository:IGenericRepository):
        super().__init__('league', LeagueEntity, LeagueModel)
        self.__race_info_repository = race_info_repository
        self.__league_ranking_repository = RankingLeagueRepository()
        self.__person_repository = person_repository

    def get_all_raw(self) -> List[LeagueRaw]:
        league_models: List[LeagueModel] = self.get_all()

        persons:List[PersonModel] = self.__person_repository.get_all()

        race_info_raw_models:List[RaceInfoRawModel] = self.__race_info_repository.get_all_raw()
        ranking_league_raw_models: List[RankingLeagueModel] = self.__league_ranking_repository.get_all()

        league_raw_results:List[LeagueRaw] = []

        for league_model in league_models:
            league_raw_model = LeagueRaw()
            league_raw_model.id = league_model.id
            league_raw_model.name = league_model.name
            league_raw_model.order = league_model.order
            
            # runner_participant_updated = []
            for runner_participant in league_model.runner_participants:
                for person in persons:
                    if person.id == runner_participant.person_id:
                        runner_participant.id = person.id
                        runner_participant.first_name = person.first_name
                        runner_participant.last_name = person.last_name
                        runner_participant.gender = person.gender
                        runner_participant.photo_url = person.photo_url

            league_raw_model.runner_participants = league_model.runner_participants

            # for race_league_raw_model in race_info_raw_models:
            #     for league_entity_race in league_model.races:
            #         if league_entity_race.race_info_id == race_league_raw_model.id:
            #             new_race_league_model = RaceLeagueRawModel()
            #             new_race_league_model.race_info = race_league_raw_model
            #             new_race_league_model.order = league_entity_race.order
            #             new_race_league_model.runners = race_league_raw_model.race_data.runners
            #             league_raw_model.races.append(new_race_league_model)

            for ranking_league_raw_model in ranking_league_raw_models:
                if ranking_league_raw_model.id == league_model.ranking_id:
                    league_raw_model.ranking_latest = ranking_league_raw_model
                if ranking_league_raw_model.id in league_model.history_ranking_ids:
                    league_raw_model.history_ranking.append(ranking_league_raw_model)

            league_raw_results.append(league_raw_model)

        return league_raw_results

    def get_raw_by_id(self, model_id:str) -> LeagueRaw:
        return None
