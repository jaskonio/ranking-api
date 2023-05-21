from typing import List
from .FactoryDownloader import FactoryDownloader
from ..model.RunnerModel import RunnerModel

class DownloaderService:
    def __init__(self, downloader_factory: FactoryDownloader):
        self.downloader_factory = downloader_factory

    def download_race_data(self, url: str):
        downloader = self.downloader_factory.factory_method(url)

        data:List[RunnerModel] = []

        if downloader is not None:
            data = downloader.race_data

        return data
