from typing import Literal, Optional
from app.domain.model.base_object_model import BaseObjectModel


class PersonModel(BaseObjectModel):
    id: str=''
    first_name: Optional[str]
    last_name: Optional[str]
    gender: Optional[Literal['H', 'M']]
    photo_url: Optional[str]

    @property
    def full_name(self) -> str:
        last_name = "" if self.last_name == "" else " " + self.last_name

        return f"{self.first_name}{last_name}" if self.first_name != "" or self.last_name != "" else ""

    @property
    def only_first_name(self) -> str:
        first_name = self.first_name.split(" ")[0]
        return first_name
    
    def __eq__(self, other) -> bool:
        if self is other:  # Comparar identidades
            return True

        return self.id == other.id or self.full_name.lower() == other.full_name.lower() or (self.only_first_name.lower() == other.only_first_name.lower() and self.last_name.lower())
