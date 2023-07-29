from typing import List
from app.aplication.mapper_service import dicts_to_class
from app.domain.model.person import Person
from app.domain.repository.person_repository import PersonRepository


class PersonService():

    def __init__(self, person_repository:PersonRepository) -> None:
        self.person_repository = person_repository

    def get_all(self) -> List[Person]:
        persons = self.person_repository.get_all()

        new_persons:List[Person] = dicts_to_class(Person, persons)

        return new_persons
