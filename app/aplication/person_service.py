from typing import List
from app.aplication.mapper_service import dict_to_class, dicts_to_class
from app.domain.model.person import Person
from app.domain.repository.generic_repository import GenericRepository


class PersonService():

    def __init__(self, person_repository:GenericRepository) -> None:
        self.person_repository = person_repository

    def get_all(self) -> List[Person]:
        persons = self.person_repository.get_all()

        new_persons:List[Person] = dicts_to_class(Person, persons)

        return new_persons

    def get_by_id(self, person_id) -> Person:
        person = self.person_repository.get_by_id(person_id)

        if person:
            return dict_to_class(Person, person)
        else:
            return None

    def add(self, person) -> Person:
        person_id = self.person_repository.add(person)

        person = self.person_repository.get_by_id(person_id)

        return dict_to_class(Person, person)

    def update_by_id(self, person_id:str, new_person):
        status = self.person_repository.update_by_id(person_id, new_person)

        if status:
            person = self.person_repository.get_by_id(person_id)
            return dict_to_class(Person, person)
        else:
            return { 'message': 'Error al actualizar.'}

    def delete_by_id(self, person_id):
        status = self.person_repository.delete_by_id(person_id)

        if status:
            return { 'message': 'Se ha eliminado correctamente'}
        else:
            return { 'message': 'Error al actualizar.'}
