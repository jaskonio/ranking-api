from typing import List, Optional
from bson import ObjectId
from app.domain.model.person_model import PersonModel
from app.infrastructure.mongoDB.model.person_entity import PersonEntity
from app.infrastructure.mongoDB.repository.mongo_db_repository import MongoDBRepository
from pymongo.errors import ServerSelectionTimeoutError


class PersonRepository(MongoDBRepository):
    def __init__(self):
        super().__init__('person', PersonEntity, PersonModel)

    def get_all(self) -> List[PersonModel]:
        try:
            result_dict = list(self.collection.find({}))

            if len(result_dict) == 0:
                return []

            result_entities:List[PersonEntity] = [self.entity_type(**entity) for entity in result_dict]
            models = []
            for entity in result_entities:
                model:PersonModel = entity.to_domain_model(PersonModel)
                model.full_name = model.first_name + ' ' + model.last_name
                models.append(model)
            return models
        except Exception as exception:
            self.logger.error("Error al obtener todos los registros: %s", str(exception))
            return []

    def get_by_id(self, model_id:str) -> Optional[PersonModel]:
        try:
            mongo_dict = self.collection.find_one({"_id": ObjectId(model_id)})

            if mongo_dict is None:
                return None

            entity = PersonEntity(**mongo_dict)
            model: PersonModel= entity.to_domain_model(PersonModel)
            model.full_name = model.first_name + ' ' + model.last_name
            return model
        except ServerSelectionTimeoutError as timeout_exception:
            self.logger.error(f'Time out al conectar con la base de datos: {timeout_exception}')
            raise
        except Exception as exception:
            self.logger.exception(f"Error al obtener el registro con ID {model_id}: {exception}")
            return None