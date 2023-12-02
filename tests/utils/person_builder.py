from app.domain.model.person import Person


class PersonBuilder():
    id = ''
    first_name = ''
    last_name = ''
    nationality = ''
    gender = ''
    photo = ''
    photo_url = ''

    def with_id(self, id):
        self.id = id
        return self

    def with_first_name(self, first_name):
        self.first_name = first_name
        return self

    def with_last_name(self, last_name):
        self.last_name = last_name
        return self

    def with_nationality(self, nationality):
        self.nationality = nationality
        return self

    def with_gender(self, gender):
        self.gender = gender
        return self

    def with_photo(self, photo):
        self.photo = photo
        return self

    def with_photo_url(self, photo_url):
        self.photo_url = photo_url
        return self

    def build(self):
        return Person(
            id = self.id,
            first_name = self.first_name,
            last_name = self.last_name,
            nationality = self.nationality,
            gender = self.gender,
            photo = self.photo,
            photo_url = self.photo_url
        )
