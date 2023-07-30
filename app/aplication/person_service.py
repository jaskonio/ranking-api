from typing import List
from app.domain.model.person import Person
from app.domain.repository.igeneric_repository import IGenericRepository


class PersonService():

    def __init__(self, person_repository:IGenericRepository) -> None:
        self.person_repository = person_repository

    def get_all(self) -> List[Person]:
        persons = self.person_repository.get_all()

        return persons

    def get_by_id(self, person_id) -> Person:
        person = self.person_repository.get_by_id(person_id)

        if person:
            return person
        else:
            return None

    def add(self, person) -> Person:
        person_id = self.person_repository.add(person)

        person = self.person_repository.get_by_id(person_id)

        return person

    def update_by_id(self, person_id:str, new_person):
        status = self.person_repository.update_by_id(person_id, new_person)

        if status:
            person = self.person_repository.get_by_id(person_id)
            return person
        else:
            return { 'message': 'Error al actualizar.'}

    def delete_by_id(self, person_id):
        status = self.person_repository.delete_by_id(person_id)

        if status:
            return { 'message': 'Se ha eliminado correctamente'}
        else:
            return { 'message': 'Error al actualizar.'}
