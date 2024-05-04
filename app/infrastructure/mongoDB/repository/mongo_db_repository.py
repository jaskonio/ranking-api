import logging
from typing import List, Optional
from bson import ObjectId
from app.infrastructure.mongoDB.repository.mongo_db_session import MongoDBSession
from pymongo import collection
from pymongo.errors import ServerSelectionTimeoutError
from app.domain.model.base_object_model import BaseObjectModel
from app.domain.repository.igeneric_repository import IGenericRepository
from app.infrastructure.mongoDB.model.base_mongo_entity import BaseMongoEntity


class MongoDBRepository(IGenericRepository):
    def __init__(self, collection_name:str, entity_type:BaseMongoEntity, model_type:BaseObjectModel):
        self.database = MongoDBSession()
        self.collection:collection.Collection = self.database.get_collection(collection_name)
        self.entity_type:BaseMongoEntity = entity_type
        self.model_type:BaseObjectModel = model_type
        self.logger = logging.getLogger(__name__)

    def get_all(self) -> List[BaseObjectModel]:
        try:
            result_dict = list(self.collection.find({}))

            if len(result_dict) == 0:
                return []

            result_entities:List[BaseMongoEntity] = [self.entity_type(**entity) for entity in result_dict]
            models = [entity.to_domain_model(self.model_type) for entity in result_entities]
            return models
        except Exception as exception:
            self.logger.error("Error al obtener todos los registros: %s", str(exception))
            return []

    def get_by_id(self, model_id:str) -> Optional[BaseObjectModel]:
        try:
            mongo_dict = self.collection.find_one({"_id": ObjectId(model_id)})

            if mongo_dict is None:
                return None

            entity:BaseMongoEntity = self.entity_type(**mongo_dict)
            return entity.to_domain_model(self.model_type)
        except ServerSelectionTimeoutError as timeout_exception:
            self.logger.error(f'Time out al conectar con la base de datos: {timeout_exception}')
            raise
        except Exception as exception:
            self.logger.exception(f"Error al obtener el registro con ID {model_id}: {exception}")
            return None

    def add(self, new_model: BaseObjectModel) -> Optional[BaseObjectModel]:
        try:
            entity:BaseMongoEntity = self.entity_type().create_by_domain_model(new_model)
            entity_id = self.collection.insert_one(entity.to_dict_db()).inserted_id

            return self.get_by_id(entity_id)
        except Exception as exception:
            self.logger.error("Error al agregar un nuevo registro: %s", str(exception))
            return None

    def update_by_id(self, model_id:str, new_model:BaseObjectModel) -> Optional[BaseObjectModel]:
        try:
            entity:BaseMongoEntity = self.entity_type().create_by_domain_model(new_model)
            dict_update = entity.to_dict_db()
            result = self.collection.update_one({"_id": ObjectId(model_id)},
                                                {"$set": dict_update})

            if result.modified_count == 0:
                return None

            return self.get_by_id(model_id)
        except Exception as exception:
            self.logger.error("Error al actualizar el registro con ID %s: %s", str(model_id), str(exception))
            return None

    def delete_by_id(self, model_id:str) -> bool:
        try:
            result = self.collection.delete_one({"_id": ObjectId(model_id)})
            return result.deleted_count > 0
        except Exception as exception:
            self.logger.error("Error al eliminar el registro con ID %s: %s", str(model_id), str(exception))
            return False
