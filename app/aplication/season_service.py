from typing import List
from app.aplication.exceptions import MethodNotImplemented
from app.aplication.league_service import LeagueService
from app.domain.model.season_model import SeasonModel, SeasonRawModel
from app.infrastructure.mongoDB.model.season_entity import SeasonEntity
from app.infrastructure.repository.repository_utils import load_repository_from_config


class SeasonService():

    def __init__(self) -> None:
        db = load_repository_from_config()
        self.__season_repository = db.get_repository('season', SeasonEntity)
        self.__leagues_service = LeagueService()

    def get_all(self) -> List[SeasonModel]:
        results: List[SeasonEntity] = self.__season_repository.get_all()

        models = [result.to_domain_model(SeasonModel) for result in results]

        return models

    def get_by_id(self, season_id) -> SeasonModel:
        result:SeasonEntity = self.__season_repository.get_by_id(season_id)

        return result.to_domain_model(SeasonModel)

    def add(self, new_model:SeasonModel) -> SeasonModel:
        season_id = self.__season_repository.add(SeasonEntity().create_by_domain_model(new_model))

        entity:SeasonEntity = self.__season_repository.get_by_id(season_id)

        return entity.to_domain_model(SeasonModel)

    def delete_by_id(self, season_id) -> bool:
        status = self.__season_repository.delete_by_id(season_id)

        if status:
            return status

        return None

    def update_by_id(self, season_id:str, new_model:SeasonModel) -> SeasonModel:
        status = self.__season_repository.update_by_id(season_id, SeasonEntity().create_by_domain_model(new_model))

        if status:
            entity:SeasonEntity = self.__season_repository.get_by_id(season_id)
            return entity.to_domain_model(SeasonModel)
        else:
            return None

    # Raw
    def get_all_raw(self) -> List[SeasonModel]:
        season_entities: List[SeasonEntity] = self.__season_repository.get_all()
        league_models = self.__leagues_service.get_all_raw()

        season_models:List[SeasonModel] = []

        for season_entity in season_entities:
            season_model:SeasonRawModel = season_entity.to_domain_model(SeasonRawModel)

            for league_model in league_models:
                if league_model.id in season_entity.league_ids:
                    season_model.leagues.append(league_model)

            season_models.append(season_model)

        return season_models

    def get_raw_by_id(self, season_id:str) -> SeasonModel:
        season_entity: SeasonEntity = self.__season_repository.get_by_id(season_id)
        league_models = self.__leagues_service.get_all_raw()

        season_model:SeasonRawModel = season_entity.to_domain_model(SeasonRawModel)

        for league_model in league_models:
            if league_model.id in season_entity.league_ids:
                season_model.leagues.append(league_model)

        return season_model
