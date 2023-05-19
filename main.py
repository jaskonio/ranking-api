from fastapi import FastAPI
from pydantic import BaseModel
from Domain.FactoryDownloader import FactoryDownloader
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from Infrastructure.MongoDB.RaceList import RaceList
load_dotenv()

from Domain.Race import Race

factory_downloader = FactoryDownloader()

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RaceDownload(BaseModel):
    url: str
    order: int

@app.get("/")
def home():
    return {"Home": "Ranking-api"}


@app.post("/race/download")
def download(item: RaceDownload):
    print("download")
    print("item: " + str(item))
    
    downloader = factory_downloader.factory_method(item.url)
    ranking = []

    if downloader != None:
        ranking = downloader.race_data
        print("Se ha descargado con exito")
    else:
        print("[ERROR]: Process factory downloader")

    # Se crea el objeto carrera y se guarda en base de datos
    new_race = Race(downloader.race_name)
    new_race.order = item.order
    new_race.ranking = ranking

    ranking_ordered = new_race.get_ranking()

    raceListModel = RaceList()
    
    raceListModel.add_race(new_race)
    
    return new_race
