from ast import List
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class RaceDetail(BaseModel):
    id: int
    name: str
    url: str
    is_load: bool

config = []

@app.get("/")
def home():
    return {"Home": "Ranking-api"}

@app.get("/admin/races")
def read_race():
    return config

@app.post("/admin/race/{race_id}")
def add_race(race_id: int, race: RaceDetail):
    race.id = race_id
    config.append(race)

    return race

@app.put("/admin/race/{race_id}")
def update_race(race_id: int, new_race: RaceDetail):
    for race in config:
        if race.id == race_id:
            race.name = new_race.name
            race.url = new_race.url

    return new_race

