from logging.config import BaseConfigurator
from bson import ObjectId
from pydantic import Field, BaseModel
from app.infrastructure.mongoDB.model.OID import OID
from app.core.mapper_utils import dict_to_class

class BaseMongoModel(BaseModel):
    id: OID = Field(default_factory=OID)

    class Config(BaseConfigurator):
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


    def to_entity(self, entity_type, key_id=None):
        return dict_to_class(entity_type, self.dict(), key_id)

    @classmethod
    def from_mongo(cls, data: dict):
        if not data:
            return data
        new_id = data.pop('_id', None)
        return cls(**dict(data, id=new_id))

    def mongo(self):
        parsed = self.dict()

        parsed.pop('id')

        return parsed
