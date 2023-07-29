from typing import List
from app.domain.model.person import Person
from app.domain.repository.person_repository import PersonRepository


class PersonService():

    def __init__(self, person_repository:PersonRepository) -> None:
        self.person_repository = person_repository

    def get_all(self) -> List[Person]:
        return self.person_repository.get_all()
        