from logging.config import BaseConfigurator
from bson import ObjectId
from pydantic import BaseModel


class BaseMongoModel(BaseModel):
    class Config(BaseConfigurator):
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
