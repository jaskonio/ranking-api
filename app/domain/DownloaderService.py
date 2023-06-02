from typing import List
from app.domain.FactoryDownloader import FactoryDownloader
from app.model.RunnerModel import RunnerModel

class DownloaderService:
    def __init__(self, downloader_factory: FactoryDownloader):
        self.downloader_factory = downloader_factory

    def download_race_data(self, url: str):
        downloader = self.downloader_factory.factory_method(url)

        data:List[RunnerModel] = []

        if downloader is not None:
            data = downloader.race_data

        return data
