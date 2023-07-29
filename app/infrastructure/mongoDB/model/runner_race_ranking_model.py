from typing import List
from app.infrastructure.mongoDB.model.runner_race_detail_model import RunnerRaceDetailModel


class RunnerRaceRankingModel(RunnerRaceDetailModel):
    points: int = 0
    posiciones_ant: List[int] = []
    averages_ant: List[str] = []
    poistion_general_ant: List[int] = []
