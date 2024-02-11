
from datetime import datetime
from typing import List
from app.domain.model.runner_base import RunnerBase


class RunnerRaceRanking(RunnerBase):
    def __init__(self, id:str = '', first_name: str = '', last_name: str = '', nationality: str = '', gender: str = ''
                    , photo: str = '', photo_url: str = '', dorsal: int = 0, club: str = 'Redolat Team' , category: str = ''
                    , position: int = 0, finished: bool = True, is_disqualified: bool =  False
                    , official_time: str = '', official_pos: int = 0, official_avg_time: str = ''
                    , official_cat_pos: int = 0, official_gen_pos: int = 0 , real_time: str = '', real_pos: int = 0, real_avg_time: str = ''
                    , real_cat_pos: int = 0, real_gen_pos: int = 0
                    , points:float = 0, posiciones_ant:List[int]=None
                    , averages_ant:List[str]=None, position_general_ant:List[int] = None) -> None:
        super().__init__(id, first_name, last_name, nationality, gender, photo, photo_url, dorsal, club, category)

        self.position = position
        self.finished = finished
        self.is_disqualified = is_disqualified

        # "%H:%M:%S"
        self.official_time = official_time
        self.official_pos = official_pos
        self.official_avg_time = official_avg_time
        self.official_cat_pos = official_cat_pos
        self.official_gen_pos = official_gen_pos

        # "%H:%M:%S"
        self.real_time = real_time
        self.real_pos = real_pos
        self.real_avg_time = real_avg_time
        self.real_cat_pos = real_cat_pos
        self.real_gen_pos = real_gen_pos

        self.points = points
        self.posiciones_ant = [] if posiciones_ant is None else posiciones_ant
        self.averages_ant = [] if averages_ant is None else averages_ant
        self.position_general_ant = [] if position_general_ant is None else position_general_ant

    def __lt__(self, other):
        time_format = "%H:%M:%S"
        return datetime.strptime(self.real_time, time_format) < datetime.strptime(other.real_time, time_format)

    def __gt__(self, other):
        time_format = "%H:%M:%S"
        return datetime.strptime(self.real_time, time_format) > datetime.strptime(other.real_time, time_format)

    def __le__(self, other):
        time_format = "%H:%M:%S"
        return datetime.strptime(self.real_time, time_format) <= datetime.strptime(other.real_time, time_format)

    def __ge__(self, other):
        time_format = "%H:%M:%S"
        return datetime.strptime(self.real_time, time_format) >= datetime.strptime(other.real_time, time_format)

    def __ne__(self, other):
        return (self.first_name != other.first_name and self.last_name != other.last_name)

    def __eq__(self, other):
        return (self.first_name == other.first_name + " " + other.last_name) or (self.first_name == other.first_name and self.last_name == other.last_name)
