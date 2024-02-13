from app.infrastructure.rest_api.model.person_request import PersonRequest


class RunnerBaseRequest(PersonRequest):
    dorsal: int = 0
    club: str = ''
    category: str = ''

class RunnerLeagueRankingRequest(RunnerBaseRequest):
    position: int = 0
    points: float = 0
    pos_last_race: int = 0
    top_five: int = 0
    participations: int = 0
    best_position: str = ''
    last_position_race: int = 0
    best_avegare_peace: str = ''
    best_position_real: int = 0
