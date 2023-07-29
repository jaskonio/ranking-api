from app.infrastructure.mongoDB.model.person_model import PersonModel


class RunnerModel(PersonModel):
    dorsal: int = 0
    club: str = ''
    category: str = ''
