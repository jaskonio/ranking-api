import unittest
from unittest.mock import MagicMock

import requests
from app.domain.repository.idownloader_race_data import RaceDownloaderOptions

from app.domain.services.downloader_runners_service import DownloaderRunnersService
from app.domain.services.http_downloader_service import HTTPDownloaderService
from app.domain.services.mappe_runners_factory import MappeRunnersFactory
from app.domain.services.race_downloader_options_factory import RaceDownloaderOptionsFactory
from app.domain.services.sportmaniacs_mapper_service import SportmaniacsMapperService


class TestDownloaderRunnersService(unittest.TestCase):
    def setUp(self):
        self.http_service_mock = MagicMock(spec=HTTPDownloaderService)
        self.mapper_runners_factory_mock = MagicMock(spec=MappeRunnersFactory)
        self.race_downloader_options_factory = MagicMock(spec=RaceDownloaderOptionsFactory)

        self.downloader_service = DownloaderRunnersService(
            http_service=self.http_service_mock,
            mapper_runners_factory=self.mapper_runners_factory_mock,
            race_downloader_options_factory=self.race_downloader_options_factory
        )

    def test_get_all_runners_return_empty_list(self):
        self.http_service_mock.get_data.return_value = []
        self.mapper_runners_factory_mock.factory_method.return_value = SportmaniacsMapperService()

        race_options = RaceDownloaderOptions()
        race_options.type = ""

        result = self.downloader_service.get_all_runners(race_options)

        self.assertListEqual(result, [])

    def test_get_all_runners_return_empty_list_when_http_service_throw_error(self):
        self.http_service_mock.get_data.side_effect = requests.exceptions.RequestException()
        self.mapper_runners_factory_mock.factory_method.return_value = SportmaniacsMapperService()

        race_options = RaceDownloaderOptions()
        race_options.type = ""

        result = self.downloader_service.get_all_runners(race_options)

        self.assertListEqual(result, [])
