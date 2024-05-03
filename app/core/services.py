from app.aplication.base_service import BaseService
from app.aplication.league_service import LeagueService
from app.aplication.race_info_service import RaceInfoService
from app.aplication.race_league_service import RaceLeagueService
from app.aplication.season_service import SeasonService
from app.domain.model.participant_league_model import ParticipantLeagueModel
from app.domain.model.person_model import PersonModel
from app.domain.model.race_info_model import RaceInfoModel
from app.domain.model.ranking_league_model import RankingLeagueModel
from app.domain.model.season_model import SeasonModel
from app.domain.services.downloader_runners_service import DownloaderRunnersService
from app.domain.services.http_downloader_service import HTTPDownloaderService
from app.domain.services.mappe_runners_factory import MappeRunnersFactory
from app.domain.services.race_downloader_options_factory import RaceDownloaderOptionsFactory
from app.infrastructure.cloud.aws_repository import AWS_Repository
# from app.infrastructure.mongoDB.model.club_info_entity import ClubInfoEntity
from app.infrastructure.mongoDB.model.participant_league_entity import ParticipantLeagueEntity
from app.infrastructure.mongoDB.model.person_entity import PersonEntity
from app.infrastructure.mongoDB.model.race_info_entity import RaceInfoEntity
from app.infrastructure.mongoDB.model.ranking_league_entity import RankingLeagueEntity
from app.infrastructure.mongoDB.model.season_entity import SeasonEntity
from app.infrastructure.mongoDB.repository.league_repository import LeagueRepository
from app.infrastructure.mongoDB.repository.mongo_db_repository import MongoDBRepository
from app.infrastructure.mongoDB.repository.race_data_repository import RaceDataRepository
from app.infrastructure.mongoDB.repository.race_info_repository import RaceInfoRepository
from app.infrastructure.mongoDB.repository.race_league_repository import RaceLeagueRepository
from app.infrastructure.mongoDB.repository.seasson_repository import SeassonRepository


club_info_repository = MongoDBRepository('club_info')
race_data_repository = RaceDataRepository()
race_info_repository = RaceInfoRepository()
person_repository = MongoDBRepository('person')
season_repository = SeassonRepository()
runner_race_data_repository = MongoDBRepository('runner_race_data')
participant_league_repository = MongoDBRepository('participant_league')
aws_repository = AWS_Repository()
ranking_league_repository = MongoDBRepository('ranking_league')
race_league_repository = RaceLeagueRepository()
league_repository = LeagueRepository()

# club_service = BaseService(club_info_repository, PersonModel, ClubInfoEntity)
person_service = BaseService(person_repository, PersonModel, PersonEntity)
participant_league_service = BaseService(participant_league_repository, ParticipantLeagueModel, ParticipantLeagueEntity)
ranking_league_service = BaseService(ranking_league_repository, RankingLeagueModel, RankingLeagueEntity)

downloader_runners_service = DownloaderRunnersService(HTTPDownloaderService(), MappeRunnersFactory(), RaceDownloaderOptionsFactory())
race_info_service = RaceInfoService(race_info_repository, RaceInfoModel, RaceInfoEntity, downloader_runners_service, race_data_repository, club_info_repository, runner_race_data_repository, person_service)

race_league_service = RaceLeagueService(race_league_repository, runner_race_data_repository, race_info_service)

league_service = LeagueService(league_repository, race_league_service, ranking_league_service, race_info_service)
seasson_service = SeasonService(season_repository, SeasonModel, SeasonEntity, league_service)
