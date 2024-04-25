from logging.config import BaseConfigurator
from pydantic import BaseModel
from bson import ObjectId

from app.domain.model.base_object_model import BaseObjectModel


class BaseAPI_Model(BaseModel):
    class Config(BaseConfigurator):
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    def create_by_domain_model(self, domain_data: BaseModel):
        data_dict = domain_data.dict()
        data = self.parse_obj(data_dict)

        return data

    def to_domain_model(self, domain_class_name:BaseObjectModel):
        data = self.dict()
        new_id = ObjectId() if 'id' not in data or data['id'] == '' else ObjectId(data['id'])
        data['id'] = str(new_id)
        new_model = domain_class_name.parse_obj(data)

        return new_model
