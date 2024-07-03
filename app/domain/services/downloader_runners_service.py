import logging
import requests
from typing import List
from app.domain.model.club_info_model import ClubInfoModel
from app.domain.model.race_data_model import RunnerRaceDataModel
from app.domain.model.race_info_model import Platform, RaceModel
from app.domain.repository.idownloader_service import IDownloaderService
from app.domain.repository.igeneric_repository import IGenericRepository
from app.infrastructure.downloader_services.downloader_service import DownloaderService
from app.infrastructure.downloader_services.spormaniacs.http_request_spormaniacs_v1_service import HttpRequestSportmaniacsV1Service
from app.infrastructure.downloader_services.spormaniacs.http_request_spormaniacs_v2_service import HttpRequestSportmaniacsV2Service
from app.infrastructure.downloader_services.spormaniacs.spormaniacs_dowloader_v1_service import SportmaniacsDownloaderV1Service
from app.infrastructure.downloader_services.spormaniacs.spormaniacs_dowloader_v2_service import SportmaniacsDownloaderV2Service


class DownloaderRunnersService:
    def __init__(self, club_info_repository:IGenericRepository):
        self.logger = logging.getLogger(__name__)
        self.__club_info_repository = club_info_repository

    def get_club_names(self):
        club_info_model_names  = []
        club_info_model:ClubInfoModel =self.__club_info_repository.get_all()
    
        if len(club_info_model) == 0:
            raise TypeError("Falta informacion del club")
        else:
            club_info_model = club_info_model[0]
            club_info_model_names = [name.lower() for name in club_info_model.names]

        return club_info_model_names

    def get_all_runners(self, race_info_simplified_model: RaceModel) -> List[RunnerRaceDataModel]:
        try:
            dowloader_service:IDownloaderService = None
            club_names = self.get_club_names()

            if race_info_simplified_model.platform == Platform.SPORTMANIACS_V1 or race_info_simplified_model.platform == Platform.SPORTMANIACS_LATEST:
                dowloader_service = DownloaderService(race_info_simplified_model, HttpRequestSportmaniacsV1Service(requests), SportmaniacsDownloaderV1Service(club_names))
            elif race_info_simplified_model.platform == Platform.SPORTMANIACS_V2:
                dowloader_service = DownloaderService(race_info_simplified_model, HttpRequestSportmaniacsV2Service(requests), SportmaniacsDownloaderV2Service(club_names))

            runners = dowloader_service.get_data()

            return runners
        except Exception as exception_error:
            self.logger.error("Error retrieving item: %s", exception_error)
            raise TypeError('An error occurred while get_all_runners') from None
