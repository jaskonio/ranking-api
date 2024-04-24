from pydantic import BaseModel

from app.core.mapper_utils import dict_to_class


class BaseAPI_Model(BaseModel):
    def to_entity(self, entity_type, key_id=None):
        return dict_to_class(entity_type, self.dict(), key_id)