from typing import List
from Model.RunnerBaseModel import RunnerBaseModel
from Model.RunnerResultModel import RunnerResultModel

class RunnerModel(RunnerBaseModel, RunnerResultModel):
    puntos: int
    posiciones_ant: List[int]
