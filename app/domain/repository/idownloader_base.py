from app.domain.repository.idownloader_race_data import IDownloaderServiceOption


class IDownloaderBase():
    def get_data(self, option:IDownloaderServiceOption):
        pass
