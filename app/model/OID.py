from bson import ObjectId
from pydantic import InvalidDiscriminator
import pydantic

class OID(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            a = ObjectId(str(v))
            return a
        except Exception as e:
            raise ValueError("Not a valid ObjectId")

# fix ObjectId & FastApi conflict
pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str
pydantic.json.ENCODERS_BY_TYPE[OID]=str