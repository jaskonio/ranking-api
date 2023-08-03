from app.domain.repository.idownloader_race_data import IDownloaderServiceOption


class IDownloaderService():
    def get_data(self, option:IDownloaderServiceOption):
        pass
