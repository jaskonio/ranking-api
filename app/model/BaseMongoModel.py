from pydantic import BaseConfig, BaseModel
from bson import ObjectId

class BaseMongoModel(BaseModel):

    class Config(BaseConfig):
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    @classmethod
    def from_mongo(cls, data: dict):
        """We must convert _id into "id". """
        if not data:
            return data
        id = data.pop('_id', None)
        return cls(**dict(data, id=id))
    
    def mongo(self, **kwargs):
        exclude_unset = kwargs.pop('exclude_unset', True)
        by_alias = kwargs.pop('by_alias', True)

        # parsed = self.dict(
        #     exclude_unset=exclude_unset,
        #     by_alias=by_alias,
        #     **kwargs,
        # )

        #parsed = self.dict(exclude_unset=exclude_unset, exclude_defaults=True)
        #parsed = self.dict(exclude_defaults=True)
        parsed = self.dict()

        # Mongo uses `_id` as default key. We should stick to that as well.
        #if '_id' not in parsed and 'id' in parsed:
            #parsed['_id'] = parsed.pop('id')
        
        parsed.pop('id')

        return parsed