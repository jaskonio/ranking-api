from app.domain.repository.idownloader_race_data import IDownloaderServiceOption
from app.domain.services.factory_downloader import FactoryDownloader


class DownloaderService:
    def __init__(self, downloader_factory: FactoryDownloader):
        self.downloader_factory = downloader_factory

    def download_race_data(self, options: IDownloaderServiceOption):
        downloader = self.downloader_factory.factory_method(options)

        data = []

        if downloader is not None:
            data = downloader.get_data(options)

        return data
