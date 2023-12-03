from app.domain.model.race import Race
from app.domain.repository.idownloader_race_data import RaceDownloaderOptions, TypePlatformInscriptions, TypeService


class RaceDownloaderOptionsFactory():
    def factory_method(self, race:Race):
        print("Factory Mapper. Type:" + str(race.platform_inscriptions_type))

        options = RaceDownloaderOptions()

        if race.platform_inscriptions_type == TypePlatformInscriptions.SPORTMANIACS_LATEST:
            race_url_splitted = race.url.split('/')
            race_id = 'default_race_id'

            if len(race_url_splitted) >= 1:
                race_id = race_url_splitted[-1]

            options.type = TypeService.SPORTMANIACS
            options.method = 'GET'
            options.url = 'https://sportmaniacs.com/es/races/rankings/' + race_id
            options.race_name = race.name

            return options

        if race.platform_inscriptions_type == TypePlatformInscriptions.VALENCIACIUDADDELRUNNING_LATEST:
            options.type = TypeService.VALENCIACIUDADDELRUNNING

            return options

        if race.platform_inscriptions_type == TypePlatformInscriptions.TOPRUN_LATEST:
            options.type = TypeService.TOPRUN

            return options

        raise ValueError("Platform Inscriptions Type not supported.")
