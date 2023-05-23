from pydantic import BaseModel

class RunnerBaseModel(BaseModel):
    dorsal: int
    name: str = ''
    club: str = 'Redolat Team'
    nationality: str = ''
    gender: str = ''
    category: str = ''
