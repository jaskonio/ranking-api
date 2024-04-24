from logging.config import BaseConfigurator
from pydantic import BaseModel, Field
from app.infrastructure.mongoDB.model.OID import OID
from app.core.mapper_utils import dict_to_class
from bson import ObjectId


class EntityBaseMongoModel(BaseModel):
    id: OID = Field(default_factory=OID)

    class Config(BaseConfigurator):
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    @classmethod
    def from_mongo(cls, data: dict):
        if not data:
            return data
        new_id = data.pop('_id', None)
        return cls(**dict(data, id=new_id))

    def to_mongo(self):
        parsed = self.dict()

        parsed.pop('id')

        return parsed

    def to_entity(self, entity_type, key_id=None):
        return dict_to_class(entity_type, self.dict(), key_id)

    def to_dict(self):
        # Si el objeto es una instancia de dict, simplemente lo devolvemos
        if isinstance(self, dict):
            return self

        # Si el objeto es una instancia de una clase personalizada, convertimos sus atributos
        if hasattr(self, '__dict__'):
            obj_dict = vars(self)

            # Convertir recursivamente los atributos que también sean objetos
            for key, value in obj_dict.items():
                if isinstance(value, (list, tuple)):
                    obj_dict[key] = [item.to_dict() if hasattr(item, '__dict__') else item for item in value]
                elif hasattr(value, '__dict__'):
                    obj_dict[key] = value.to_dict

            return obj_dict

        # Si el objeto no es una instancia de una clase personalizada, simplemente lo devolvemos
        return self
