from app.domain.model.base_object_model import BaseObjectModel


class PersonModel(BaseObjectModel):
    id: str=''
    first_name: str | None = None
    first_name: str | None = None
    last_name: str| None = None
    gender: str| None = None
    photo_url: str| None = None

    def __eq__(self, other_person):
        if self.id == other_person.person_id:
            return True

        self_full_name = self.first_name + ' ' + self.last_name
        other_full_name = other_person.first_name + ' ' + other_person.last_name

        if self_full_name.lower().strip() == other_full_name.lower().strip():
            return True

        return False
