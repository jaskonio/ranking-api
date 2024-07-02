from typing import List
from app.domain.model.race_data_model import RunnerRaceDataModel


class IDownloaderService():
    def get_data(self) -> List[RunnerRaceDataModel]:
        pass

class IHttpRequestService:
    def request_data(self, url: str) -> dict:
        pass

class IRunnerDataProcessor:
    def process_data(self, data: dict) -> List[RunnerRaceDataModel]:
        pass