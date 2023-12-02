from typing import List
from app.infrastructure.mongoDB.model.runner_model import RunnerModel


class RunnerRaceDetailModel(RunnerModel):      
    position: int = 0
    finished: bool = False
    is_disqualified: bool = False

    # "%H:%M:%S"
    official_time: str = ''
    official_pos: int = 0
    official_avg_time: str = ''
    official_cat_pos: str = ''
    official_gen_pos: str = ''

    # "%H:%M:%S"
    real_time: str = ''
    real_pos: int = 0
    real_avg_time: str = ''
    real_cat_pos: str = ''
    real_gen_pos: str = ''

    points: float = 0
    posiciones_ant: List[int] = []
    averages_ant: List[str] = []
    position_general_ant: List[int] = []
