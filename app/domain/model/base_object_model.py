from app.core.mapper_utils import class_to_dict, dict_to_class
from pydantic import BaseModel

class BaseObjectModel(BaseModel):
    def to_dict(self):
        return class_to_dict(self)

    def to_entity(self, entity_type):
        return dict_to_class(entity_type, self.dict())
