from logging.config import BaseConfigurator
from pydantic import BaseModel, Field
from app.infrastructure.mongoDB.model.OID import OID
from app.core.mapper_utils import dict_to_class
from bson import ObjectId


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

    # def to_dict(self):
    #     # Si el objeto es una instancia de dict, simplemente lo devolvemos
    #     if isinstance(self, dict):
    #         return self

    #     # Si el objeto es una instancia de una clase personalizada, convertimos sus atributos
    #     if hasattr(self, '__dict__'):
    #         obj_dict = vars(self)

    #         # Convertir recursivamente los atributos que también sean objetos
    #         for key, value in obj_dict.items():
    #             if isinstance(value, (list, tuple)):
    #                 obj_dict[key] = [item.to_dict() if hasattr(item, '__dict__') else item for item in value]
    #             elif hasattr(value, '__dict__'):
    #                 obj_dict[key] = value.to_dict

    #         return obj_dict

    #     # Si el objeto no es una instancia de una clase personalizada, simplemente lo devolvemos
    #     return self
