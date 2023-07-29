
from typing import List
from app.domain.model.runner_race_detail import RunnerRaceDetail


class RunnerRaceRanking(RunnerRaceDetail):
    def __init__(self, first_name: str, last_name: str = '', nationality: str = '', gender: str = ''
                 , photo: str = '', photo_url: str = '', dorsal: int = 0, club: str = 'Redolat Team'
                 , category: str = '', position: int = 0, finished: bool = True
                 , official_time: str = '', official_pos: int = 0, official_avg_time: str = ''
                    , official_cat_pos: int = 0, official_gen_pos: int = 0
                , real_time: str = '', real_pos: int = 0, real_avg_time: str = ''
                , real_cat_pos: int = 0, real_gen_pos: int = 0
                ,points:float = 0, posiciones_ant:List[int]=None, averages_ant:List[str]=None
                ,poistion_general_ant:List[int] = None) -> None:
        super().__init__(first_name, last_name, nationality, gender, photo, photo_url, dorsal, club
                         , category, position, finished, official_time, official_pos
                         , official_avg_time, official_cat_pos, official_gen_pos, real_time
                         , real_pos, real_avg_time, real_cat_pos, real_gen_pos)
        self.points = points
        self.posiciones_ant = posiciones_ant
        self.averages_ant = averages_ant
        self.poistion_general_ant = poistion_general_ant
