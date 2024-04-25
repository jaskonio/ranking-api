from app.domain.model.base_object_model import BaseObjectModel


class PersonModel(BaseObjectModel):
    id: str=''
    first_name: str = ''
    last_name:str = ''
    nationality: str = ''
    gender: str = ''
    photo_url: str = ''

    def __eq__(self, other_person):
        return self.id == other_person.id and self.first_name == other_person.first_name and self.last_name == other_person.last_name
