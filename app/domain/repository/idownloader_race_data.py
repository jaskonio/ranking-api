from enum import Enum

class TypeService(Enum):
    SPORTMANIACS = 1
    VALENCIACIUDADDELRUNNING = 2
    TOPRUN = 3

class DownloaderHTTPOptions():
    type: TypeService
    method: str
    url: str
    payload: None
    content_type: str
    timeout: int = 30

class RaceDownloaderOptions(DownloaderHTTPOptions):
    race_name: str

class IDownloaderRaceData():
    def get_data(self, option:DownloaderHTTPOptions):
        pass
