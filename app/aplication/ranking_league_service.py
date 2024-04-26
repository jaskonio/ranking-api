from typing import List
from app.domain.model.ranking_league_model import RankingLeagueModel
from app.infrastructure.mongoDB.model.ranking_league_entity import RankingLeagueEntity
from app.infrastructure.repository.repository_utils import load_repository_from_config


class RankingLeagueService():

    def __init__(self) -> None:
        db = load_repository_from_config()
        self.__ranking_league_repository = db.get_repository('ranking_league', RankingLeagueEntity)

    def get_all(self) -> List[RankingLeagueModel]:
        participant_league_entity: List[RankingLeagueEntity] = self.__ranking_league_repository.get_all()
        return [participant_league_entity.to_domain_model(RankingLeagueModel) for participant_league_entity in participant_league_entity]

    def get_by_id(self, ranking_league_id:str) -> RankingLeagueModel:
        participant_league_entity:RankingLeagueEntity = self.__ranking_league_repository.get_by_id(ranking_league_id)

        if participant_league_entity is None:
            return None

        return participant_league_entity.to_domain_model(RankingLeagueModel)

    def add(self, new_person:RankingLeagueModel) -> RankingLeagueModel:
        ranking_league_id = self.__ranking_league_repository.add(RankingLeagueEntity().create_by_domain_model(new_person))

        participant_league_entity:RankingLeagueEntity = self.__ranking_league_repository.get_by_id(ranking_league_id)

        return participant_league_entity.to_domain_model(RankingLeagueModel)

    def update_by_id(self, ranking_league_id:str, new_person:RankingLeagueModel):
        status = self.__ranking_league_repository.update_by_id(ranking_league_id, RankingLeagueEntity().create_by_domain_model(new_person))

        if status:
            participant_league_entity:RankingLeagueEntity = self.__ranking_league_repository.get_by_id(ranking_league_id)
            return participant_league_entity.to_domain_model(RankingLeagueModel)
        else:
            return None

    def delete_by_id(self, ranking_league_id: str) -> bool:
        status = self.__ranking_league_repository.delete_by_id(ranking_league_id)

        if status:
            return status

        return None
