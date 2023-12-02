from app.domain.repository.idownloader_race_data import DownloaderHTTPOptions


class IDownloaderBase():
    def get_data(self, option:DownloaderHTTPOptions):
        pass
