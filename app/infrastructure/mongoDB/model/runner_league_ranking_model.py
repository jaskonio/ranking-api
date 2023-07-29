from app.infrastructure.mongoDB.model.person_model import PersonModel


class RunnerLeagueRankingModel(PersonModel):
    position: int = 0
    points: int = 0
    pos_last_race: int = 0
    top_five: int = 0
    participations: int = 0
    best_position: str = ''
    last_position_race: int = 0
    best_avegare_peace: str = ''
    best_position_real: int = 0
