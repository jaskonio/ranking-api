from typing import Optional
from app.infrastructure.mongoDB.model.base_mongo_entity import BaseMongoEntity


class RunnerRaceDataEntity(BaseMongoEntity):
    first_name: Optional[str]
    last_name: Optional[str]
    nationality: str = ''
    gender: str = ''
    photo_url: str = ''

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
