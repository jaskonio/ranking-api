from app.aplication.base_service import BaseService
from app.aplication.league_service import LeagueService
from app.aplication.race_info_service import RaceInfoService
from app.domain.model.club_info_model import ClubInfoModel
from app.domain.model.participant_league_model import ParticipantLeagueModel
from app.domain.model.person_model import PersonModel
from app.domain.model.runner_race_data_model import RunnerRaceDataModel
from app.domain.services.downloader_runners_service import DownloaderRunnersService
from app.domain.services.http_downloader_service import HTTPDownloaderService
from app.domain.services.mappe_runners_factory import MappeRunnersFactory
from app.domain.services.race_downloader_options_factory import RaceDownloaderOptionsFactory
from app.infrastructure.cloud.aws_repository import AWS_Repository
from app.infrastructure.mongoDB.model.club_info_entity import ClubInfoEntity
from app.infrastructure.mongoDB.model.participant_league_entity import ParticipantLeagueEntity
from app.infrastructure.mongoDB.model.person_entity import PersonEntity
from app.infrastructure.mongoDB.model.runner_race_data_entity import RunnerRaceDataEntity
from app.infrastructure.mongoDB.repository.league_repository import LeagueRepository
from app.infrastructure.mongoDB.repository.mongo_db_repository import MongoDBRepository
from app.infrastructure.mongoDB.repository.race_data_repository import RaceDataRepository
from app.infrastructure.mongoDB.repository.race_info_repository import RaceInfoRepository
from app.infrastructure.mongoDB.repository.race_league_repository import RaceLeagueRepository
from app.infrastructure.mongoDB.repository.ranking_league_repository import RankingLeagueRepository
from app.infrastructure.mongoDB.repository.seasson_repository import SeassonRepository


club_info_repository = MongoDBRepository('club_info', ClubInfoEntity, ClubInfoModel)
race_data_repository = RaceDataRepository()
race_info_repository = RaceInfoRepository()
person_repository = MongoDBRepository('person', PersonEntity, PersonModel)
season_repository = SeassonRepository()
runner_race_data_repository = MongoDBRepository('runner_race_data', RunnerRaceDataEntity, RunnerRaceDataModel)
participant_league_repository = MongoDBRepository('participant_league', ParticipantLeagueEntity, ParticipantLeagueModel)
aws_repository = AWS_Repository()
ranking_league_repository = RankingLeagueRepository()
race_league_repository = RaceLeagueRepository()
league_repository = LeagueRepository()

# club_service = BaseService(club_info_repository, PersonModel, ClubInfoEntity)
person_service = BaseService(person_repository)
participant_league_service = BaseService(participant_league_repository)
ranking_league_service = BaseService(ranking_league_repository)
race_league_service = BaseService(race_league_repository)
seasson_service = BaseService(season_repository)

downloader_runners_service = DownloaderRunnersService(HTTPDownloaderService(), MappeRunnersFactory(), RaceDownloaderOptionsFactory())
race_info_service = RaceInfoService(race_info_repository, downloader_runners_service, race_data_repository, club_info_repository, runner_race_data_repository, person_repository)
league_service = LeagueService(league_repository, ranking_league_repository)
