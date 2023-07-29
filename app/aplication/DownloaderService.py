from app.aplication.factory_downloader import FactoryDownloader


class DownloaderService:
    def __init__(self, downloader_factory: FactoryDownloader):
        self.downloader_factory = downloader_factory

    def download_race_data(self, url: str):
        downloader = self.downloader_factory.factory_method(url)

        data = []

        if downloader is not None:
            data = downloader.race_data

        return data
