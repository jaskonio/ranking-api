"""_summary_
"""
from typing import List
from app.model.runner_base_model import RunnerBaseModel
from app.model.RunnerResultModel import RunnerResultModel

class RunnerModel(RunnerBaseModel, RunnerResultModel):
    """_summary_

    Args:
        RunnerBaseModel (_type_): _description_
        RunnerResultModel (_type_): _description_
    """
    position: int = 0
    puntos: int = 0
    photo_data = ''
    posiciones_ant: List[int] = []
    averages_ant: List[str] = []
    poistion_general_ant: List[int] = []
