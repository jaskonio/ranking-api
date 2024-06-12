from typing import Dict, List
from app.domain.model.person_model import PersonModel
from app.domain.model.runner_race_data_model import RunnerRaceDataModel
from app.infrastructure.mongoDB.model.person_entity import PersonEntity
from app.infrastructure.mongoDB.model.runner_race_data_entity import RunnerRaceDataEntity
from app.infrastructure.mongoDB.repository.mongo_db_repository import MongoDBRepository

class RunnerRaceDataRepository(MongoDBRepository):
    def __init__(self):
        super().__init__('runner_race_data', RunnerRaceDataEntity, RunnerRaceDataModel)
        self.__person_repository = MongoDBRepository('person', PersonEntity, PersonModel)
    
    def get_all(self):
        try:
            results_dict = list(self.collection.find({}))

            if len(results_dict) == 0:
                return []

            result_entities:List[RunnerRaceDataEntity] = [RunnerRaceDataEntity(**entity) for entity in results_dict]
            runner_race_data_models:List[RunnerRaceDataModel] = [entity.to_domain_model(RunnerRaceDataModel) for entity in result_entities]
            
            # all_persons:List[PersonModel] = self.__person_repository.get_all()
            # all_persons_dict:Dict[str, PersonModel] = {}
            
            # for person in all_persons:
                # all_persons_dict[person.id] = person
            
            # for runner_race_data_model in runner_race_data_models:
            #     if runner_race_data_model.person_id in all_persons_dict:
            #         person = all_persons_dict[runner_race_data_model.person_id]
            #         runner_race_data_model.first_name = person.first_name
            #         runner_race_data_model.last_name = person.last_name
            #         runner_race_data_model.gender = person.gender
            #         runner_race_data_model.photo_url = person.photo_url
                    
            return runner_race_data_models
        except Exception as exception:
            self.logger.error("Error al obtener todos los registros: %s", str(exception))
            return []