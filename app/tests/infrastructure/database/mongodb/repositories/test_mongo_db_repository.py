import unittest
from unittest.mock import patch
from bson import ObjectId
import mongomock

from app.domain.model.base_object_model import BaseObjectModel
from app.infrastructure.mongoDB.model.base_mongo_entity import BaseMongoEntity
from app.infrastructure.mongoDB.repository.mongo_db_repository import MongoDBRepository


# Mocks for domain model and entity
class MockModel(BaseObjectModel):
    id: str = ''
    name: str = 'test'

class MockEntity(BaseMongoEntity):
    id: str = ''
    name: str = 'test'

    @staticmethod
    def create_by_domain_model(domain_model: BaseObjectModel):
        return MockEntity(id=domain_model.id, name=domain_model.name)

    def to_domain_model(self, model_type: BaseObjectModel):
        return model_type(id=self.id, name=self.name)

class TestMongoDBRepository(unittest.TestCase):

    @patch('app.infrastructure.mongoDB.repository.mongo_db_session.MongoDBSession.get_collection')
    def setUp(self, mock_get_collection):
        # Mock the MongoDB collection
        self.mock_collection = mongomock.MongoClient().db.collection
        mock_get_collection.return_value = self.mock_collection

        # Initialize the repository
        self.repository = MongoDBRepository('mock_collection', MockEntity, MockModel)

    def test_get_all(self):
        # Insert mock data
        self.mock_collection.insert_one({'_id': ObjectId(), 'name': 'test'})

        # Call the method
        result = self.repository.get_all()

        # Check assertions
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, 'test')

    def test_get_by_id(self):
        # Insert mock data
        mock_id = ObjectId()
        self.mock_collection.insert_one({'_id': mock_id, 'name': 'test'})

        # Call the method
        result = self.repository.get_by_id(str(mock_id))

        # Check assertions
        self.assertIsNotNone(result)
        self.assertEqual(result.name, 'test')

    def test_get_by_id_not_found(self):
        # Call the method with a non-existing ID
        result = self.repository.get_by_id(str(ObjectId()))
        self.assertEqual(result, None)

    def test_add(self):
        # Create a mock model
        mock_model = MockModel(id=str(ObjectId()), name='test')

        # Call the method
        result = self.repository.add(mock_model)

        # Check assertions
        self.assertIsNotNone(result)
        self.assertEqual(result.name, 'test')

    def test_update_by_id(self):
        # Insert mock data
        mock_id = ObjectId()
        self.mock_collection.insert_one({'_id': mock_id, 'name': 'test'})

        # Create a mock model with updated data
        updated_model = MockModel(id=str(mock_id), name='updated')

        # Call the method
        result = self.repository.update_by_id(str(mock_id), updated_model)

        # Check assertions
        self.assertIsNotNone(result)
        self.assertEqual(result.name, 'updated')

    def test_delete_by_id(self):
        # Insert mock data
        mock_id = ObjectId()
        self.mock_collection.insert_one({'_id': mock_id, 'name': 'test'})

        # Call the method
        result = self.repository.delete_by_id(str(mock_id))

        # Check assertions
        self.assertTrue(result)
        self.assertIsNone(self.mock_collection.find_one({'_id': mock_id}))

    def test_delete_by_id_not_found(self):
        # Call the method with a non-existing ID
        result = self.repository.delete_by_id(str(ObjectId()))

        # Check assertions
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
