import unittest
from app.domain.repository.idownloader_race_data import DownloaderHTTPOptions, TypeService
from app.domain.services.mappe_runners_factory import MappeRunnersFactory
from app.domain.services.sportmaniacs_mapper_service import SportmaniacsMapperService


class TestMapperRunnersFactory(unittest.TestCase):

    def setUp(self):
        self.factory = MappeRunnersFactory()

    def test_factory_method_sportmaniacs(self):
        http_options = DownloaderHTTPOptions()
        http_options.type = TypeService.SPORTMANIACS

        result = self.factory.factory_method(http_options)
        self.assertIsInstance(result, SportmaniacsMapperService)

    def test_factory_method_unknown_type(self):
        http_options = DownloaderHTTPOptions()
        http_options.type = ''

        with self.assertRaises(ValueError):
            self.factory.factory_method(http_options)

if __name__ == '__main__':
    unittest.main()
