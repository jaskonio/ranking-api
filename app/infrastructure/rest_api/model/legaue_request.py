from typing import List
from app.infrastructure.mongoDB.model.base_mongo_model import BaseMongoModel


class LeagueRequest(BaseMongoModel):
    name: str
    races:List[dict] = []
    ranking:List[dict] = []
    runners:List[dict] = []
