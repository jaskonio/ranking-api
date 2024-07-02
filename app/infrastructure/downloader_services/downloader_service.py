from typing import List
from app.domain.model.race_data_model import RunnerRaceDataModel
from app.domain.model.race_info_model import RaceModel
from app.domain.repository.idownloader_service import IDownloaderService, IHttpRequestService, IRunnerDataProcessor

class DownloaderService(IDownloaderService):
    def __init__(self, race_info: RaceModel, request_service: IHttpRequestService, data_processor: IRunnerDataProcessor):
        self.race_info = race_info
        self.request_service = request_service
        self.data_processor = data_processor

    def get_data(self) -> List[RunnerRaceDataModel]:
        try:
            response_json = self.request_service.request_data(self.race_info.url)
            return self.data_processor.process_data(response_json)
        except Exception as exception_error:
            raise TypeError(f'Error processing request: {exception_error}')
