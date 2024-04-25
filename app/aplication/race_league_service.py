from typing import List
from app.domain.model.race_league_model import RaceLeagueModel
from app.infrastructure.mongoDB.model.race_league_entity import RaceLeagueEntity
from app.infrastructure.repository.repository_utils import load_repository_from_config

class RaceLeagueService():

    def __init__(self):
        db = load_repository_from_config()
        self.__race_info_repository = db.get_repository('race_league', RaceLeagueEntity)

    def get_all(self) -> List[RaceLeagueModel]:
        race_entities:List[RaceLeagueEntity] = self.__race_info_repository.get_all()

        return [race_entity.to_domain_model(RaceLeagueModel) for race_entity in race_entities]

    def get_by_id(self, race_id:str) -> RaceLeagueModel:
        race_entity:RaceLeagueEntity = self.__race_info_repository.get_by_id(race_id)

        return race_entity.to_domain_model(RaceLeagueModel)

    def add(self, new_race: RaceLeagueModel) -> RaceLeagueModel:
        race_id = self.__race_info_repository.add(RaceLeagueEntity().create_by_domain_model(new_race))

        race_entity:RaceLeagueEntity = self.__race_info_repository.get_by_id(race_id)

        return race_entity.to_domain_model(RaceLeagueModel)

    def update_by_id(self, race_id:str, new_race:RaceLeagueModel) -> RaceLeagueModel:
        status = self.__race_info_repository.update_by_id(race_id, RaceLeagueEntity().create_by_domain_model(new_race))

        if status:
            race_entity:RaceLeagueEntity = self.__race_info_repository.get_by_id(race_id)
            return race_entity.to_domain_model(RaceLeagueModel)
        else:
            return None

    def delete_by_id(self, race_id) -> bool:
        status = self.__race_info_repository.delete_by_id(race_id)

        if status:
            return status

        return None
