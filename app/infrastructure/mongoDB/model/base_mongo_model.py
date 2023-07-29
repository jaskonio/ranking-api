import datetime
from logging.config import BaseConfigurator
from bson import ObjectId
from pydantic import Field, BaseModel
from app.infrastructure.mongoDB.model.OID import OID


class BaseMongoModel(BaseModel):
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

    def mongo(self):
        # exclude_unset = kwargs.pop('exclude_unset', True)
        # by_alias = kwargs.pop('by_alias', True)

        # parsed = self.dict(
        #     exclude_unset=exclude_unset,
        #     by_alias=by_alias,
        #     **kwargs,
        # )

        #parsed = self.dict(exclude_unset=exclude_unset, exclude_defaults=True)
        #parsed = self.dict(exclude_defaults=True)
        # parsed = self.dict()
        parsed = {}

        #parsed =  vars(self)
        #parsed = self.__dict__
        parsed = class_to_dict(self)

        # Mongo uses `_id` as default key. We should stick to that as well.
        #if '_id' not in parsed and 'id' in parsed:
            #parsed['_id'] = parsed.pop('id')

        parsed.pop('id')

        return parsed

def class_to_dict(obj):
    # Si el objeto es una instancia de dict, simplemente lo devolvemos
    if isinstance(obj, dict):
        return obj

    # Si el objeto es una instancia de una clase personalizada, convertimos sus atributos
    if hasattr(obj, '__dict__'):
        obj_dict = vars(obj)

        # Convertir recursivamente los atributos que también sean objetos
        for key, value in obj_dict.items():
            if isinstance(value, (list, tuple)):
                obj_dict[key] = [class_to_dict(item) if hasattr(item, '__dict__') else item for item in value]
            elif hasattr(value, '__dict__'):
                obj_dict[key] = class_to_dict(value)

        return obj_dict

    # Si el objeto no es una instancia de una clase personalizada, simplemente lo devolvemos
    return obj