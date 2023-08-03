from app.domain.repository.idownloader_race_data import IDownloaderServiceOption
from app.domain.repository.idownloader_service import IDownloaderService
from app.domain.services.downloader_sportmaniacs_service import DownloaderSportmaniacsService
from app.domain.services.http_downloader_service import HTTPDownloaderService


class FactoryDownloader:
    def factory_method(self, options: IDownloaderServiceOption):
        print("FactoryDownloader. factory_method. options" + str(options))
        downloader:IDownloaderService = IDownloaderService()

        if 'sportmaniacs' in options.type:
            print("Platform: Sportmaniacs")
            downloader = DownloaderSportmaniacsService(HTTPDownloaderService())

        elif 'valenciaciudaddelrunning' in options.type:
            print("Platform: valenciaciudaddelrunning")
            #downloader = Valenciaciudaddelrunning(url_race)

        elif 'toprun' in options.type:
            print("Platform: toprun")
            #downloader = TopRun(url_race)
        else:
            print("Platform not compatible")

        return downloader
