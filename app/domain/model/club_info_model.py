from typing import List
from app.domain.model.base_object_model import BaseObjectModel


class ClubInfoModel(BaseObjectModel):
    names: List[str] = []
