from pydantic import BaseConfig, BaseModel, Field
from bson import ObjectId
from app.model.OID import OID


class BaseMongoModel(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_

    Returns:
        _type_: _description_
    """
    id: OID = Field(default_factory=OID)

    class Config(BaseConfig):
        """_summary_

        Args:
            BaseConfig (_type_): _description_
        """
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    @classmethod
    def from_mongo(cls, data: dict):
        """We must convert _id into "id". """
        if not data:
            return data
        new_id = data.pop('_id', None)
        return cls(**dict(data, id=new_id))

    def mongo(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        # exclude_unset = kwargs.pop('exclude_unset', True)
        # by_alias = kwargs.pop('by_alias', True)

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
