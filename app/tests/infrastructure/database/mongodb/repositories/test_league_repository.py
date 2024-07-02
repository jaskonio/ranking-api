import unittest
from unittest.mock import patch, MagicMock
from bson import ObjectId
from pymongo.errors import ServerSelectionTimeoutError, PyMongoError
from app.domain.model.league_model import LeagueModel
from app.domain.repository.igeneric_repository import IGenericRepository
from app.infrastructure.exceptions import RepositoryConnectionError, RepositoryOperationError
from app.infrastructure.mongoDB.model.league_entity import LeagueEntity
from app.infrastructure.mongoDB.repository.league_repository import LeagueRepository
from app.infrastructure.mongoDB.repository.race_info_repository import RaceInfoRepository

class TestLeagueRepository(unittest.TestCase):
    @patch('app.infrastructure.mongoDB.repository.mongo_db_repository.MongoDBSession.get_collection')
    def setUp(self, mock_get_collection):
        self.mock_collection = MagicMock()
        mock_get_collection.return_value = self.mock_collection

        self.mock_race_info_repository = MagicMock(spec=RaceInfoRepository)
        self.mock_person_repository = MagicMock(spec=IGenericRepository)

        self.league_repository = LeagueRepository(
            race_info_repository=self.mock_race_info_repository,
            person_repository=self.mock_person_repository
        )

    def test_get_all_empty(self):
        self.mock_collection.find.return_value = []
        self.mock_person_repository.get_all.return_value = []
        self.mock_race_info_repository.get_all.return_value = []

        result = self.league_repository.get_all()
        self.assertEqual(result, [])

    def test_get_all(self):
        league_data = {"_id": ObjectId(), "name": "Test League", "order": 1}
        self.mock_collection.find.return_value = [league_data]
        self.mock_person_repository.get_all.return_value = []
        self.mock_race_info_repository.get_all.return_value = []

        result = self.league_repository.get_all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Test League")

    def test_get_by_id_not_found(self):
        self.mock_collection.find_one.return_value = None

        result = self.league_repository.get_by_id(str(ObjectId()))
        self.assertIsNone(result)

    def test_get_by_id(self):
        league_data = {"_id": ObjectId(), "name": "Test League", "order": 1}
        self.mock_collection.find_one.return_value = league_data
        self.mock_person_repository.get_all.return_value = []
        self.mock_race_info_repository.get_all.return_value = []

        result = self.league_repository.get_by_id(str(ObjectId()))
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "Test League")

    def test_update_by_id_success(self):
        league_model = LeagueModel(id=str(ObjectId()), name="Updated League", order=2)
        league_data = {"_id": ObjectId(), "name": "Updated League", "order": 2}

        self.mock_collection.update_one.return_value = MagicMock(matched_count=1)
        self.mock_collection.find_one.return_value = league_data
        
        result = self.league_repository.update_by_id(str(ObjectId()), league_model)
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "Updated League")

    def test_add_success(self):
        league_model = LeagueModel(id=str(ObjectId()), name="New League", order=1)
        league_entity = LeagueEntity(name="New League", order=1)
        
        self.mock_collection.insert_one.return_value.inserted_id = ObjectId()
        self.mock_collection.find_one.return_value = league_entity.to_dict_db()
        
        with patch.object(LeagueEntity, 'create_by_domain_model', return_value=league_entity):
            result = self.league_repository.add(league_model)
            self.assertIsNotNone(result)
            self.assertEqual(result.name, "New League")

    # Exceptions
    def test_get_all_connection_error(self):
        self.mock_collection.find.side_effect = ServerSelectionTimeoutError("Timeout error")
        
        with self.assertRaises(RepositoryConnectionError):
            self.league_repository.get_all()

    def test_get_all_operation_error(self):
        self.mock_collection.find.side_effect = PyMongoError("General error")
        
        with self.assertRaises(RepositoryOperationError):
            self.league_repository.get_all()

    def test_get_by_id_connection_error(self):
        self.mock_collection.find_one.side_effect = ServerSelectionTimeoutError("Timeout error")
        
        with self.assertRaises(RepositoryConnectionError):
            self.league_repository.get_by_id(str(ObjectId()))

    def test_get_by_id_operation_error(self):
        self.mock_collection.find_one.side_effect = PyMongoError("General error")
        
        with self.assertRaises(RepositoryOperationError):
            self.league_repository.get_by_id(str(ObjectId()))

    def test_add_connection_error(self):
        league_model = LeagueModel(id=str(ObjectId()), name="New League", order=1)
        self.mock_collection.insert_one.side_effect = ServerSelectionTimeoutError("Timeout error")
        
        with self.assertRaises(RepositoryConnectionError):
            self.league_repository.add(league_model)

    def test_add_operation_error(self):
        league_model = LeagueModel(id=str(ObjectId()), name="New League", order=1)
        self.mock_collection.insert_one.side_effect = PyMongoError("General error")
        
        with self.assertRaises(RepositoryOperationError):
            self.league_repository.add(league_model)

    def test_delete_by_id_connection_error(self):
        self.mock_collection.delete_one.side_effect = ServerSelectionTimeoutError("Timeout error")
        
        with self.assertRaises(RepositoryConnectionError):
            self.league_repository.delete_by_id(str(ObjectId()))

    def test_delete_by_id_operation_error(self):
        self.mock_collection.delete_one.side_effect = PyMongoError("General error")
        
        with self.assertRaises(RepositoryOperationError):
            self.league_repository.delete_by_id(str(ObjectId()))

    def test_update_by_id_connection_error(self):
        league_model = LeagueModel(id=str(ObjectId()), name="Updated League", order=2)
        self.mock_collection.update_one.side_effect = ServerSelectionTimeoutError("Timeout error")
        
        with self.assertRaises(RepositoryConnectionError):
            self.league_repository.update_by_id(str(ObjectId()), league_model)

    def test_update_by_id_operation_error(self):
        league_model = LeagueModel(id=str(ObjectId()), name="Updated League", order=2)
        self.mock_collection.update_one.side_effect = PyMongoError("General error")
        
        with self.assertRaises(RepositoryOperationError):
            self.league_repository.update_by_id(str(ObjectId()), league_model)

if __name__ == '__main__':
    unittest.main()
