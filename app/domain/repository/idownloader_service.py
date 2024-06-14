from typing import List
from app.domain.model.race_data_model import RunnerRaceDataModel


class IDownloaderService():
    def get_data(self) -> List[RunnerRaceDataModel]:
        pass
