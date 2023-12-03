from app.domain.model.runner_base import RunnerBase

class RunnerBaseBuilder:
    def __init__(self):
        self.id = '1'
        self.first_name = 'John'
        self.last_name = 'Doe'
        self.nationality = 'US'
        self.gender = 'Male'
        self.photo = 'base64encodedphoto'
        self.photo_url = '/person/image/1'
        self.dorsal = 123
        self.club = 'Redolat Team'
        self.category = 'Senior'

    def with_id(self, id):
        self.id = id
        return self

    def with_name(self, first_name, last_name):
        self.first_name = first_name
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

    def with_dorsal(self, dorsal):
        self.dorsal = dorsal
        return self

    def with_club(self, club):
        self.club = club
        return self

    def with_category(self, category):
        self.category = category
        return self

    def build(self):
        return RunnerBase(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            nationality=self.nationality,
            gender=self.gender,
            photo=self.photo,
            photo_url=self.photo_url,
            dorsal=self.dorsal,
            club=self.club,
            category=self.category
        )
