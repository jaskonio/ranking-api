
from app.domain.model.runner_base import RunnerBase


class RunnerLeagueRanking(RunnerBase):
    def __init__(self, id:str='', first_name: str='', last_name: str = '', nationality: str = '', gender: str = ''
                 , photo: str = '', photo_url: str = '', dorsal:int = 0, club: str = 'Redolat Team' , category: str = ''
                 , position:int = 0, points:float = 0, pos_last_race:int = 0, top_five:int = 0
                 , participations:int = 0, best_position:str = '', last_position_race:int = 0
                 , best_avegare_peace:str = '', best_position_real:int = 0) -> None:
        super().__init__(id, first_name, last_name, nationality, gender, photo, photo_url, dorsal, club, category)
        self.position = position
        self.points = points
        self.pos_last_race = pos_last_race
        self.top_five = top_five
        self.participations = participations
        self.best_position = best_position
        self.last_position_race = last_position_race
        self.best_avegare_peace = best_avegare_peace
        self.best_position_real = best_position_real
