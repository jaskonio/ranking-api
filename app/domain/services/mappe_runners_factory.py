from app.domain.repository.idownloader_race_data import DownloaderHTTPOptions, TypeService
from app.domain.services.sportmaniacs_mapper_service import SportmaniacsMapperService

class MappeRunnersFactory:
    def factory_method(self, http_options: DownloaderHTTPOptions):
        print("Factory Mapper. Type:" + str(http_options.type))

        if http_options.type == TypeService.SPORTMANIACS:
            print("Platform: Sportmaniacs")
            mapper = SportmaniacsMapperService()

        if http_options.type == TypeService.VALENCIACIUDADDELRUNNING:
            print("Platform: valenciaciudaddelrunning")
            #mapper = Valenciaciudaddelrunning(url_race)

        if http_options.type == TypeService.TOPRUN:
            print("Platform: toprun")
            #mapper = TopRun(url_race)
        else:
            print("Platform not compatible")

        return mapper
