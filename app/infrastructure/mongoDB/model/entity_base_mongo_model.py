from pydantic import Field
from app.infrastructure.mongoDB.model.base_mongo_model import BaseMongoModel
from app.infrastructure.mongoDB.model.OID import OID
from app.core.mapper_utils import dict_to_class


class EntityBaseMongoModel(BaseMongoModel):
    id: OID = Field(default_factory=OID)

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
