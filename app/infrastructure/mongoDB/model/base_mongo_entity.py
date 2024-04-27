from logging.config import BaseConfigurator
from typing import List
from pydantic import BaseModel, Field
from app.infrastructure.mongoDB.model.OID import OID
from bson import ObjectId


def db_list_dict_to_entites(entity_class_name, datas:List[dict]):
    entities = []

    for data in datas:
        entity = db_dict_to_build_entity(entity_class_name, data)
        entities.append(entity)

    return entities

def db_dict_to_build_entity(entity_class_name, data:dict):
    new_id = data.pop('_id', None)
    data["id"] = new_id

    entity = entity_class_name(**dict(data))
    return entity

class BaseMongoEntity(BaseModel):
    id: OID = Field(default_factory=OID)

    class Config(BaseConfigurator):
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    def create_by_domain_model(self, domain_data: BaseModel):
        data_dict = domain_data.dict()

        new_id = ObjectId() if 'id' not in data_dict or data_dict['id'] == '' else ObjectId(data_dict['id'])
        data_dict['id'] = new_id

        data = self.parse_obj(data_dict)

        return data

    def to_dict_db(self):
        parsed = self.dict()

        parsed.pop('id')

        return parsed

    def to_domain_model(self, class_model:BaseModel):
        data = self.dict()
        new_class = class_model.parse_obj(data)
        return new_class

    def to_dict(self):
        return self.dict()
