import unittest
from app.domain.repository.idownloader_race_data import TypePlatformInscriptions, TypeService
from app.domain.services.race_downloader_options_factory import RaceDownloaderOptionsFactory
from tests.utils.race_builder import RaceBuilder

class TestRaceDownloaderOptionsFactory(unittest.TestCase):
    def setUp(self):
        self.factory = RaceDownloaderOptionsFactory()

    def test_factory_method_sportmaniacs(self):
        race = RaceBuilder(id='fake_id_01', name='TestRace', url='test_url/id_01').with_platform_inscriptions(TypePlatformInscriptions.SPORTMANIACS_LATEST).build()
        options = self.factory.factory_method(race)

        self.assertEqual(options.type, TypeService.SPORTMANIACS)
        self.assertEqual(options.method, 'GET')
        self.assertEqual(options.url, 'https://sportmaniacs.com/es/races/rankings/id_01')
        self.assertEqual(options.race_name, 'TestRace')

    def test_factory_method_sportmaniacs_url_not_contain_id_valid(self):
        race = RaceBuilder(id='fake_id_01', name='TestRace', url='test_url').with_platform_inscriptions(TypePlatformInscriptions.SPORTMANIACS_LATEST).build()
        options = self.factory.factory_method(race)

        self.assertEqual(options.type, TypeService.SPORTMANIACS)
        self.assertEqual(options.method, 'GET')
        self.assertEqual(options.url, 'https://sportmaniacs.com/es/races/rankings/test_url')
        self.assertEqual(options.race_name, 'TestRace')

    def test_factory_method_sportmaniacs_not_contain_url(self):
        race = RaceBuilder(id='fake_id_01', name='TestRace', url='').with_platform_inscriptions(TypePlatformInscriptions.SPORTMANIACS_LATEST).build()
        options = self.factory.factory_method(race)

        self.assertEqual(options.type, TypeService.SPORTMANIACS)
        self.assertEqual(options.method, 'GET')
        self.assertEqual(options.url, 'https://sportmaniacs.com/es/races/rankings/')
        self.assertEqual(options.race_name, 'TestRace')

    def test_factory_method_valenciaciudaddelrunning(self):
        race = RaceBuilder(id='fake_id_01', name='TestRace', url='test_url').with_platform_inscriptions(TypePlatformInscriptions.VALENCIACIUDADDELRUNNING_LATEST).build()
        options = self.factory.factory_method(race)

        self.assertEqual(options.type, TypeService.VALENCIACIUDADDELRUNNING)

    def test_factory_method_toprun(self):
        race = RaceBuilder(id='fake_id_01', name='TestRace', url='test_url').with_platform_inscriptions(TypePlatformInscriptions.TOPRUN_LATEST).build()
        options = self.factory.factory_method(race)

        self.assertEqual(options.type, TypeService.TOPRUN)

    def test_factory_method_invalid_platform(self):
        race = RaceBuilder(id='fake_id_01', name='TestRace', url='test_url').with_platform_inscriptions('asdasd').build()
        with self.assertRaises(ValueError):
            self.factory.factory_method(race)

if __name__ == '__main__':
    unittest.main()
