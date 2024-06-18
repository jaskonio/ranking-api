import logging
from typing import List, Optional
from bson import ObjectId
from app.infrastructure.exceptions import handle_repository_exceptions
from app.infrastructure.mongoDB.repository.mongo_db_session import MongoDBSession
from pymongo import collection
from app.domain.model.base_object_model import BaseObjectModel
from app.domain.repository.igeneric_repository import IGenericRepository
from app.infrastructure.mongoDB.model.base_mongo_entity import BaseMongoEntity


class MongoDBRepository(IGenericRepository):
    def __init__(self, collection_name:str, entity_type:BaseMongoEntity, model_type:BaseObjectModel):
        self.collection:collection.Collection = MongoDBSession.get_collection(collection_name)
        self.entity_type:BaseMongoEntity = entity_type
        self.model_type:BaseObjectModel = model_type
        self.logger = logging.getLogger(__name__)

    @handle_repository_exceptions
    def get_all(self) -> List[BaseObjectModel]:
        result_dict = list(self.collection.find({}))

        if len(result_dict) == 0:
            return []

        result_entities:List[BaseMongoEntity] = [self.entity_type(**entity) for entity in result_dict]
        models = [entity.to_domain_model(self.model_type) for entity in result_entities]
        return models

    @handle_repository_exceptions
    def get_by_id(self, model_id:str) -> Optional[BaseObjectModel]:
        mongo_dict = self.collection.find_one({"_id": ObjectId(model_id)})

        if mongo_dict is None:
            return None

        entity:BaseMongoEntity = self.entity_type(**mongo_dict)
        return entity.to_domain_model(self.model_type)

    @handle_repository_exceptions
    def add(self, new_model: BaseObjectModel) -> Optional[BaseObjectModel]:
        entity:BaseMongoEntity = self.entity_type().create_by_domain_model(new_model)
        entity_id = self.collection.insert_one(entity.to_dict_db()).inserted_id
        return self.get_by_id(entity_id)

    @handle_repository_exceptions
    def update_by_id(self, model_id:str, new_model:BaseObjectModel) -> Optional[BaseObjectModel]:
        entity:BaseMongoEntity = self.entity_type().create_by_domain_model(new_model)
        dict_update = entity.to_dict_db()
        self.collection.update_one({"_id": ObjectId(model_id)}, {"$set": dict_update})
        return self.get_by_id(model_id)

    @handle_repository_exceptions
    def delete_by_id(self, model_id:str) -> bool:
        result = self.collection.delete_one({"_id": ObjectId(model_id)})
        return result.deleted_count > 0

