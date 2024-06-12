from typing import List
from app.domain.model.league_model import LeagueModel, LeagueRAWModel
from app.domain.model.person_model import PersonModel
from app.domain.model.race_info_model import RaceInfoRawModel
from app.domain.model.race_league_model import RaceLeagueRawModel
from app.domain.repository.igeneric_repository import IGenericRepository
from app.infrastructure.mongoDB.model.league_entity import LeagueEntity
from app.infrastructure.mongoDB.model.person_entity import PersonEntity
from app.infrastructure.mongoDB.repository.mongo_db_repository import MongoDBRepository
from app.infrastructure.mongoDB.repository.race_data_repository import RaceDataRepository
from app.infrastructure.mongoDB.repository.race_info_repository import RaceInfoRepository
from app.infrastructure.mongoDB.repository.race_league_repository import RaceLeagueRepository
from app.infrastructure.mongoDB.model.participant_league_entity import ParticipantLeagueEntity
from app.infrastructure.mongoDB.model.ranking_league_entity import RankingLeagueEntity
from app.domain.model.participant_league_model import ParticipantLeagueModel
from app.domain.model.ranking_league_model import RankingLeagueModel
from app.infrastructure.mongoDB.repository.ranking_league_repository import RankingLeagueRepository


class LeagueRepository(MongoDBRepository):
    def __init__(self, race_info_repository:IGenericRepository, person_repository:IGenericRepository):
        super().__init__('league', LeagueEntity, LeagueModel)
        self.__race_info_repository = race_info_repository
        self.__ranking_league_service = RankingLeagueRepository()
        self.__person_repository = person_repository

    def get_all_raw(self) -> List[LeagueRAWModel]:
        league_models: List[LeagueModel] = self.get_all()

        return []

    def get_raw_by_id(self, model_id:str) -> LeagueRAWModel:
        league_entity: LeagueEntity = self.get_by_id(model_id)

        race_info_raw_models:List[RaceInfoRawModel] = self.__race_info_repository.get_all_raw()
        person_models: List[PersonModel] = self.__person_repository.get_all()
        ranking_league_raw_models: List[RankingLeagueModel] = self.__ranking_league_service.get_all()

        league_raw_model = LeagueRAWModel()
        league_raw_model.id = league_entity.id
        league_raw_model.name = league_entity.name

        for race_league_raw_model in race_info_raw_models:
            for league_entity_race in league_entity.races:
                if league_entity_race.race_info_id == race_league_raw_model.id:
                    new_race_league_model = RaceLeagueRawModel()
                    new_race_league_model.race_info = race_league_raw_model
                    new_race_league_model.order = league_entity_race.order
                    new_race_league_model.runners = race_league_raw_model.race_data.runners
                    league_raw_model.races.append(new_race_league_model)

        for ranking_league_raw_model in ranking_league_raw_models:
            if ranking_league_raw_model.id == league_entity.ranking_id:
                league_raw_model.ranking_latest = ranking_league_raw_model
            if ranking_league_raw_model.id in league_entity.history_ranking_ids:
                league_raw_model.history_ranking.append(ranking_league_raw_model)

        for runner_participant in league_entity.runner_participants:
            for person_model in person_models:
                if runner_participant.person_id == person_model.id:
                    participant_model = ParticipantLeagueModel()
                    participant_model.id = person_model.id
                    participant_model.first_name = person_model.first_name
                    participant_model.last_name = person_model.last_name
                    participant_model.gender = person_model.gender
                    participant_model.photo_url = person_model.photo_url
                    
                    participant_model.person_id = person_model.id

                    participant_model.dorsal = runner_participant.dorsal
                    participant_model.category = runner_participant.category
                    participant_model.disqualified_order_race = runner_participant.disqualified_order_race

                    league_raw_model.runner_participants.append(participant_model)

        return league_raw_model
