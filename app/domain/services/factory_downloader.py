from app.domain.repository.idownloader_service import IDownloaderService
from app.domain.repository.igeneric_repository import IGenericRepository
from app.domain.services.downloader_sportmaniacs_service import DownloaderSportmaniacsService
from app.domain.services.http_downloader_service import HTTPDownloaderService


class FactoryDownloader:
    def factory_method(self, url: str, person_repository:IGenericRepository):
        print("FactoryDownloader. factory_method. url" + str(url))
        downloader:IDownloaderService = IDownloaderService()

        if 'sportmaniacs' in url:
            print("Platform: Sportmaniacs")
            downloader = DownloaderSportmaniacsService(HTTPDownloaderService(), person_repository)

        elif 'valenciaciudaddelrunning' in url:
            print("Platform: valenciaciudaddelrunning")
            #downloader = Valenciaciudaddelrunning(url_race)

        elif 'toprun' in url:
            print("Platform: toprun")
            #downloader = TopRun(url_race)
        else:
            print("Platform not compatible")

        return downloader
