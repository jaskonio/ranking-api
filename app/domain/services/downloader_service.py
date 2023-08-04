from app.domain.repository.igeneric_repository import IGenericRepository
from app.domain.services.factory_downloader import FactoryDownloader


class DownloaderService:
    def __init__(self, downloader_factory: FactoryDownloader):
        self.downloader_factory = downloader_factory

    def download_race_data(self, url:str, person_repository:IGenericRepository):
        downloader = self.downloader_factory.factory_method(url, person_repository)

        data = []

        if downloader is not None:
            data = downloader.get_data(url)

        return data
