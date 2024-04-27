from typing import List
from app.domain.model.person_model import PersonModel
from app.infrastructure.mongoDB.model.person_entity import PersonEntity
from app.infrastructure.repository.repository_utils import load_repository_from_config


class PersonService():

    def __init__(self) -> None:
        db = load_repository_from_config()
        self.__person_repository = db.get_repository('person', PersonEntity)

    def get_all(self) -> List[PersonModel]:
        person_entities: List[PersonEntity] = self.__person_repository.get_all()
        return [person_entity.to_domain_model(PersonModel) for person_entity in person_entities]

    def get_by_id(self, person_id:str) -> PersonModel:
        person_entity:PersonEntity = self.__person_repository.get_by_id(person_id)

        if person_entity is None:
            return None

        return person_entity.to_domain_model(PersonModel)

    def add(self, new_person:PersonModel) -> PersonModel:
        new_person.photo_url = 'https://i.pravatar.cc/30'

        person_entity:PersonEntity = self.__person_repository.add(PersonEntity().create_by_domain_model(new_person))

        return person_entity.to_domain_model(PersonModel)

    def update_by_id(self, person_id:str, new_person:PersonModel):
        status = self.__person_repository.update_by_id(person_id, PersonEntity().create_by_domain_model(new_person))

        if status:
            person_entity:PersonEntity = self.__person_repository.get_by_id(person_id)
            return person_entity.to_domain_model(PersonModel)
        else:
            return None

    def delete_by_id(self, person_id: str) -> bool:
        status = self.__person_repository.delete_by_id(person_id)

        if status:
            return status

        return None
