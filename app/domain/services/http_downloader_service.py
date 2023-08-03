import requests
from app.domain.repository.idownloader_race_data import IDownloaderServiceOption
from app.domain.repository.idownloader_service import IDownloaderService


class HTTPDownloaderService(IDownloaderService):
    def get_data(self, option:IDownloaderServiceOption):
        results = requests.request(option.method, option.url, data=option.data
                                   , timeout=option.timeout)

        if option.after_callback is not None:
            results = option.after_callback(results)

        return results
