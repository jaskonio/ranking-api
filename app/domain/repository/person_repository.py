import abc
from typing import List

from app.domain.model.person import Person

class PersonRepository(abc.ABC):
    def get_all(self) -> List[Person]:
        pass
