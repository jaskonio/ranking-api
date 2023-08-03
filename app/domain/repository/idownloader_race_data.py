class IDownloaderServiceOption():
    type: str

class IDownloaderServiceHTTPOption(IDownloaderServiceOption):
    method: str
    url: str
    data: str = ''
    timeout: int = 30
    before_callback: classmethod(None)
    after_callback: classmethod(None)


class IDownloaderRaceData():
    def get_data(self, option:IDownloaderServiceOption):
        pass
