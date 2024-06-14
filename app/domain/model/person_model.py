from typing import Literal, Optional
from app.domain.model.base_object_model import BaseObjectModel


class PersonModel(BaseObjectModel):
    id = ''
    first_name: Optional[str]
    last_name: Optional[str]
    gender: Optional[Literal['H', 'M']]
    photo_url: Optional[str]

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __eq__(self, other) -> bool:
        if self is other:  # Comparar identidades
            return True

        return self.id == other.id or self.full_name.lower() == other.full_name.lower()
