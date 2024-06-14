from typing import List, Optional
from app.infrastructure.mongoDB.model.base_mongo_entity import BaseMongoEntity
from app.infrastructure.mongoDB.model.person_entity import PersonWithoutEntity

class RunnerRaceData(PersonWithoutEntity):
    person_id: Optional[str]
    dorsal: Optional[int]
    club: Optional[str]
    category: Optional[str]
    finished: Optional[bool]

    official_time: Optional[str]
    official_pos: Optional[int]
    official_avg_time: Optional[str]
    official_cat_pos: Optional[int]
    official_gen_pos: Optional[int]

    real_time: Optional[str]
    real_pos: Optional[int]
    real_avg_time: Optional[str]
    real_cat_pos: Optional[int]
    real_gen_pos: Optional[int]


class RaceDataEntity(BaseMongoEntity):
    runners: List[RunnerRaceData] = []
