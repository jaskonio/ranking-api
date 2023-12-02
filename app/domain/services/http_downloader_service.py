import requests
from app.domain.repository.idownloader_base import IDownloaderBase
from app.domain.repository.idownloader_race_data import DownloaderHTTPOptions


class HTTPDownloaderService(IDownloaderBase):
    def get_data(self, option:DownloaderHTTPOptions):
        try:
            if option.method.upper() == 'GET':
                response = requests.get(option.url, timeout=option.timeout)
            elif option.method.upper() == 'POST':
                response = requests.post(option.url, timeout=option.timeout, data=option.payload)

                response.raise_for_status()

            if option.content_type.upper() == 'JSON':
                contenido_parseado = response.json()
            else:
                contenido_parseado = response.content.decode('utf-8')

            return contenido_parseado

        except requests.exceptions.RequestException as e:
            raise e
