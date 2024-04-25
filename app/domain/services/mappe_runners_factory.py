import logging
from app.domain.repository.idownloader_race_data import DownloaderHTTPOptions, TypeService
from app.domain.services.sportmaniacs_mapper_service import SportmaniacsMapperService


logger = logging.getLogger(__name__)

class MappeRunnersFactory:
    def factory_method(self, http_options: DownloaderHTTPOptions):
        logger.info("Factory Mapper. Type: %s", str(http_options.type.name))

        if http_options.type == TypeService.SPORTMANIACS:
            return SportmaniacsMapperService()

        if http_options.type == TypeService.VALENCIACIUDADDELRUNNING:
            pass

        if http_options.type == TypeService.TOPRUN:
            pass

        raise ValueError("Servicion no soportado.")
