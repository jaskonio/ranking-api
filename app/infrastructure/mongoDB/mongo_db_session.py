from pymongo import MongoClient
from app.core.config import Settings
from app.domain.repository.igeneric_repository import IGenericRepository
from app.infrastructure.mongoDB.model.club_info_entity import ClubInfoEntity
from app.infrastructure.mongoDB.model.league_entity import LeagueEntity
from app.infrastructure.mongoDB.model.participant_league_entity import ParticipantLeagueEntity
from app.infrastructure.mongoDB.model.person_entity import PersonEntity
from app.infrastructure.mongoDB.model.race_data_entity import RaceDataEntity
from app.infrastructure.mongoDB.model.race_info_entity import RaceInfoEntity
from app.infrastructure.mongoDB.model.race_league_entity import RaceLeagueEntity
from app.infrastructure.mongoDB.model.ranking_league_entity import RankingLeagueEntity
from app.infrastructure.mongoDB.model.runner_race_data_entity import RunnerRaceDataEntity
from app.infrastructure.mongoDB.model.season_entity import SeasonEntity
from app.infrastructure.mongoDB.repository.mongo_db_repository import MongoDBRepository

class MongoDBSession:
    def __init__(self):
        db_name = Settings.DATABASE_NAME
        connection_string = Settings.CONNECTION_STRING + db_name

        self.client = MongoClient(connection_string)
        self.database = self.client.get_database()

db = MongoDBSession()

def get_repository(repository_name: str) -> IGenericRepository:
    if repository_name == "club_info":
        return MongoDBRepository(db.database, 'club_info', ClubInfoEntity)
    elif repository_name == "race_info":
        return MongoDBRepository(db.database, 'race_info', RaceInfoEntity)
    elif repository_name == "person":
        return MongoDBRepository(db.database, 'person', PersonEntity)
    elif repository_name == "season":
        return MongoDBRepository(db.database, 'season', SeasonEntity)
    elif repository_name == "race_league":
        return MongoDBRepository(db.database, 'race_league', RaceLeagueEntity)
    elif repository_name == "race_data":
        return MongoDBRepository(db.database, 'race_data', RaceDataEntity)
    elif repository_name == "runner_race_data":
        return MongoDBRepository(db.database, 'runner_race_data', RunnerRaceDataEntity)
    elif repository_name == "league":
        return MongoDBRepository(db.database, 'league', LeagueEntity)
    elif repository_name == "ranking_league":
        return MongoDBRepository(db.database, 'ranking_league', RankingLeagueEntity)
    elif repository_name == "participant_league":
        return MongoDBRepository(db.database, 'participant_league', ParticipantLeagueEntity)
    else:
        raise ValueError("Nombre de repositorio no válido")
