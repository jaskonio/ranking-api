from enum import Enum

class TypeService(Enum):
    SPORTMANIACS = 1
    VALENCIACIUDADDELRUNNING = 2
    TOPRUN = 3

class TypePlatformInscriptions(Enum):
    SPORTMANIACS_LATEST = 1
    VALENCIACIUDADDELRUNNING_LATEST = 2
    TOPRUN_LATEST = 3

class DownloaderHTTPOptions():
    def __init__(self):
        pass

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
