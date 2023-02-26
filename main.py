from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Race(BaseModel):
    name: str
    url: str
    is_load: Union[bool, None] = None

@app.get("/admin/race/{race_id}")
def read_race(race_id: int, q: Union[str, None] = None):
    return {"race_id": race_id, "q": q}

@app.put("/admin/race/{race_id}")
def update_race(race_id: int, race: Race):
    return {"race_name": race.name, "race_id": race_id}
