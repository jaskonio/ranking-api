from typing import List
from pydantic import BaseModel

class RunnerModel(BaseModel):
    dorsal: int
    name: str
    club: str
    nationality: str
    finished: bool
    gender: str
    category: str
    officialTime: str
    officialPos: str
    officialAverageTime: str
    officialCatPos: str
    officialGenPos: str
    realTime: str
    realPos: str
    realAverageTime: str
    realCatPos: str
    realGenPos: str
    puntos: int
    posiciones_ant: List[int]
