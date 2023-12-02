from app.infrastructure.mongoDB.model.person_model import PersonModel


class RunnerModel(PersonModel):
    dorsal: str = ''
    club: str = ''
    category: str = ''
