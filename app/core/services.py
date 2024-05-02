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
from app.infrastructure.mongoDB.mongo_db_session import get_repository


club_info_repository = get_repository('club_info')
race_info_repository = get_repository('race_info')
person_repository = get_repository('person')
season_repository = get_repository('season')
race_league_repository = get_repository('race_league')
race_data_repository = get_repository('race_data')
runner_race_data_repository = get_repository('runner_race_data')
league_repository = get_repository('league')
ranking_league_repository = get_repository('ranking_league')
participant_league_repository = get_repository('participant_league')
aws_repository = AWS_Repository()

# club_service = BaseService(club_info_repository, PersonModel, ClubInfoEntity)
person_service = BaseService(person_repository, PersonModel, PersonEntity)
participant_league_service = BaseService(participant_league_repository, ParticipantLeagueModel, ParticipantLeagueEntity)
ranking_league_service = BaseService(ranking_league_repository, RankingLeagueModel, RankingLeagueEntity)

downloader_runners_service = DownloaderRunnersService(HTTPDownloaderService(), MappeRunnersFactory(), RaceDownloaderOptionsFactory())
race_info_service = RaceInfoService(race_info_repository, RaceInfoModel, RaceInfoEntity, downloader_runners_service, race_data_repository, club_info_repository, runner_race_data_repository, person_service)

race_league_service = RaceLeagueService(race_league_repository, runner_race_data_repository, race_info_service)

league_service = LeagueService(league_repository, race_league_service, participant_league_service, ranking_league_service, race_info_service)
seasson_service = SeasonService(season_repository, SeasonModel, SeasonEntity, league_service)
