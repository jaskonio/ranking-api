from typing import List
from app.domain.model.person_model import PersonModel
from app.domain.model.ranking_league_model import RankingLeagueModel
from app.infrastructure.mongoDB.model.person_entity import PersonEntity
from app.infrastructure.mongoDB.model.ranking_league_entity import RankingLeagueEntity
from app.infrastructure.mongoDB.repository.mongo_db_repository import MongoDBRepository


class RankingLeagueRepository(MongoDBRepository):
    def __init__(self):
        super().__init__('ranking_league', RankingLeagueEntity, RankingLeagueModel)
        self.__person_repository = MongoDBRepository('person', PersonEntity, PersonModel)

    def get_all(self) -> List[RankingLeagueModel]:
        try:
            result_dict = list(self.collection.find({}))

            if len(result_dict) == 0:
                return []
    
            ranking_league_entities:List[RankingLeagueEntity] = [RankingLeagueEntity(**result) for result in result_dict]
            ranking_league_models:List[RankingLeagueModel] = [ranking_league_entity.to_domain_model(RankingLeagueModel) for ranking_league_entity in ranking_league_entities]
    
            all_person:List[PersonModel] = self.__person_repository.get_all()

            for ranking_league_model in ranking_league_models:
                for runner in ranking_league_model.data:
                    for person in all_person:
                        if person.id == runner.person_id:
                            runner.last_name = person.last_name
                            runner.first_name = person.first_name
                            runner.gender = person.gender
                            runner.photo_url = person.photo_url

            return ranking_league_models
        except Exception as exception:
            self.logger.error("Error al obtener todos los registros: %s", str(exception))
            return []