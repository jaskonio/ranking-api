from app.domain.model.race_info_model import Platform, RaceInfoSimplifiedModel
from app.domain.repository.idownloader_race_data import RaceDownloaderOptions, TypeService


class RaceDownloaderOptionsFactory():
    def factory_method(self, race_info_model: RaceInfoSimplifiedModel):
        print("Factory Mapper. Type:" + str(race_info_model.platform))

        options = RaceDownloaderOptions()

        if race_info_model.platform == Platform.SPORTMANIACS_LATEST:
            race_url_splitted = race_info_model.url.split('/')
            race_id = 'default_race_id'

            if len(race_url_splitted) >= 1:
                race_id = race_url_splitted[-1]

            options.type = TypeService.SPORTMANIACS
            options.method = 'GET'
            options.url = 'https://sportmaniacs.com/es/races/rankings/' + race_id
            options.race_name = race_info_model.name
            options.content_type = "JSON"

            return options

        if race_info_model.platform == Platform.VALENCIACIUDADDELRUNNING_LATEST:
            options.type = TypeService.VALENCIACIUDADDELRUNNING

            return options

        if race_info_model.platform == Platform.TOPRUN_LATEST:
            options.type = TypeService.TOPRUN

            return options

        raise ValueError("Platform Inscriptions Type not supported.")
