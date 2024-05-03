from logging.config import BaseConfigurator
from bson import ObjectId
from pydantic import BaseModel, Field
from app.domain.model.base_object_model import BaseObjectModel
from app.infrastructure.mongoDB.model.OID import OID


class BaseMongoEntity(BaseModel):
    id: OID = Field(default_factory=OID,alias="_id")

    class Config(BaseConfigurator):
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    def create_by_domain_model(self, domain_data: BaseObjectModel):
        data_dict = domain_data.dict()

        new_id = ObjectId() if 'id' not in data_dict or data_dict['id'] == '' else ObjectId(data_dict['id'])
        data_dict['id'] = new_id

        data = self.parse_obj(data_dict)

        return data

    def to_dict_db(self):
        parsed = self.dict()

        parsed.pop('id')

        return parsed

    def to_domain_model(self, class_model:BaseObjectModel):
        data = self.dict()
        new_class = class_model.parse_obj(data)
        return new_class

    def to_dict(self):
        return self.dict()
