from typing import List
from pydantic import Field
from app.infrastructure.rest_api.model.race_base_request import RaceBaseRequest


class RaceRequest(RaceBaseRequest):
    order: int = 0
    is_sorted: bool = False
    ranking: List[dict] = Field(default_factory=list)
    participants = []
