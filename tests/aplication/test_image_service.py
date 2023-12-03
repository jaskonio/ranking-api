import unittest
from unittest.mock import MagicMock
from app.aplication.image_service import ImageService
from app.domain.repository.igeneric_repository import IGenericRepository


class TestImageService(unittest.TestCase):
    def setUp(self):
        self.person_repository_mock = MagicMock(spec=IGenericRepository)
        self.image_service = ImageService(person_repository=self.person_repository_mock)

    def test_get_image_by_person_id_person_not_found(self):
        person_id = 2

        # Mocking the person_repository.get_by_id method
        self.person_repository_mock.get_by_id.return_value = None

        # Testing the get_image_by_person_id method when person is not found
        result = self.image_service.get_image_by_person_id(person_id)

        # Assertions
        self.assertIsNone(result)
        self.person_repository_mock.get_by_id.assert_called_once_with(person_id)

if __name__ == '__main__':
    unittest.main()
