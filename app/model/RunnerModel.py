from typing import List
from .RunnerBaseModel import RunnerBaseModel
from .RunnerResultModel import RunnerResultModel

class RunnerModel(RunnerBaseModel, RunnerResultModel):
    puntos: int
    posiciones_ant: List[int]
