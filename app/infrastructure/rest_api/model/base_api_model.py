from logging.config import BaseConfigurator
from pydantic import BaseModel
from bson import ObjectId


class BaseAPI_Model(BaseModel):
    class Config(BaseConfigurator):
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    def to_class_entity(self, class_entity):
        data = self.dict()
        new_id = ObjectId() if 'id' not in data or data['id'] == '' else ObjectId(data['id'])
        data['id'] = new_id
        new_entity = class_entity(**dict(data))
        return new_entity
