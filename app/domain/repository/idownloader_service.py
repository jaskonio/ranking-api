from typing import List
from app.domain.model.race_info_model import RaceInfoModel
from app.domain.model.runner_race_data_model import RunnerRaceDataModel


class IDownloaderService():
    def get_data(self) -> List[RunnerRaceDataModel]:
        pass
