from pydantic import BaseModel
import datetime

format = "%H:%M:%S"

class RunnerResultModel(BaseModel):
    finished: bool = True
    officialTime: str = datetime.datetime.now().strftime(format)
    officialPos: int = 0
    officialAverageTime: str = ''
    officialCatPos: int = 0
    officialGenPos: int = 0
    realTime: str = datetime.datetime.now().strftime(format)
    realPos: int = 0
    realAverageTime: str = ''
    realCatPos: int = 0
    realGenPos: int = 0
