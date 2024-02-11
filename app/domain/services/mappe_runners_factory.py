from app.domain.repository.idownloader_race_data import DownloaderHTTPOptions, TypeService
from app.domain.services.sportmaniacs_mapper_service import SportmaniacsMapperService

class MappeRunnersFactory:
    def factory_method(self, http_options: DownloaderHTTPOptions):
        print("Factory Mapper. Type:" + str(http_options.type.name))

        if http_options.type == TypeService.SPORTMANIACS:
            return SportmaniacsMapperService()

        if http_options.type == TypeService.VALENCIACIUDADDELRUNNING:
            pass

        if http_options.type == TypeService.TOPRUN:
            pass

        raise ValueError("Servicion no soportado.")
