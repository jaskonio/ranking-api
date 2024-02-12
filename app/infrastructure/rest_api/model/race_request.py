from typing import List
from pydantic import Field
from app.infrastructure.mongoDB.model.base_mongo_model import BaseMongoModel


class RaceRequest(BaseMongoModel):
    name: str
    url: str
    raw_ranking: List[dict] = Field(default_factory=list)
    platform_inscriptions:int = 1
    processed:bool = False
