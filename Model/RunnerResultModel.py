from pydantic import BaseModel

class RunnerResultModel(BaseModel):
    finished: bool
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
