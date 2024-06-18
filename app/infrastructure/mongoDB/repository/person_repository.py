from typing import List, Optional
from bson import ObjectId
from app.domain.model.person_model import PersonModel
from app.infrastructure.exceptions import handle_repository_exceptions
from app.infrastructure.mongoDB.model.person_entity import PersonEntity
from app.infrastructure.mongoDB.repository.mongo_db_repository import MongoDBRepository
from pymongo.errors import ServerSelectionTimeoutError


class PersonRepository(MongoDBRepository):
    def __init__(self):
        super().__init__('person', PersonEntity, PersonModel)

    @handle_repository_exceptions
    def get_all(self) -> List[PersonModel]:
        result_dict = list(self.collection.find({}))

        if len(result_dict) == 0:
            return []

        result_entities:List[PersonEntity] = [self.entity_type(**entity) for entity in result_dict]
        models = []
        for entity in result_entities:
            model:PersonModel = entity.to_domain_model(PersonModel)
            model.set_full_name()
            models.append(model)
        return models

    @handle_repository_exceptions
    def get_by_id(self, model_id:str) -> Optional[PersonModel]:
        mongo_dict = self.collection.find_one({"_id": ObjectId(model_id)})

        if mongo_dict is None:
            return None

        entity = PersonEntity(**mongo_dict)
        model: PersonModel= entity.to_domain_model(PersonModel)
        model.set_full_name()

        return model
