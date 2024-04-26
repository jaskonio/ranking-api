from bson import ObjectId
import pydantic
from bson.objectid import ObjectId as BsonObjectId


class OID(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            if not isinstance(v, BsonObjectId):
                raise TypeError('ObjectId required')

            a = str(ObjectId(str(v)))
            return a
        except Exception as e:
            raise ValueError("Not a valid ObjectId")

# # fix ObjectId & FastApi conflict
pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str
pydantic.json.ENCODERS_BY_TYPE[OID]=str
