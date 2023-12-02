from app.domain.model.race import Race
from app.domain.repository.idownloader_race_data import RaceDownloaderOptions, TypePlatformInscriptions, TypeService


class RaceDownloaderOptionsFactory():
    def factory_method(self, race:Race):
        print("Factory Mapper. Type:" + str(race.platform_inscriptions_type))

        options = RaceDownloaderOptions()

        if race.platform_inscriptions_type == TypePlatformInscriptions.SPORTMANIACS_LATEST:
            options.type = TypeService.SPORTMANIACS
            options.method = 'GET'
            options.url = 'https://sportmaniacs.com/es/races/rankings/' + race.url.split('/')[-1]
            options.race_name = race.name

            return options

        if race.platform_inscriptions_type == TypePlatformInscriptions.VALENCIACIUDADDELRUNNING_LATEST:
            options.type = TypeService.VALENCIACIUDADDELRUNNING

            return options

        if race.platform_inscriptions_type == TypePlatformInscriptions.TOPRUN_LATEST:
            options.type = TypeService.TOPRUN

            return options

        raise ValueError("Platform Inscriptions Type not supported.")