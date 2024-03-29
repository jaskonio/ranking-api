from app.domain.model.base_entity import BaseEntity


class Person(BaseEntity):

    def __init__(self, id:str='', first_name: str = '', last_name:str = '', nationality: str = '',
                 gender: str = '', photo:str = '', photo_url: str = '') -> None:
        self.id = str(id)
        self.first_name = first_name
        self.last_name = last_name
        self.nationality = nationality
        self.gender = gender
        self.photo = photo
        self.photo_url = photo_url

    def __eq__(self, other_person):
        return self.id == other_person.id and self.first_name == other_person.first_name and self.last_name == other_person.last_name
