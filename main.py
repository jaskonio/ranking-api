from fastapi import FastAPI
from pydantic import BaseModel
from Domain.FactoryDownloader import FactoryDownloader
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
def home():
    return {"Home": "Ranking-api"}

@app.post("/race/download")
def download(item: RaceDownload):
    print("download")
    print("item: " + str(item))
    
    downloader = factory_downloader.factory_method(item.url)
    data = []

    if downloader != None:
        data = downloader.race_data
    else:
        print("[ERROR]: Process factory downloader")

    return data
