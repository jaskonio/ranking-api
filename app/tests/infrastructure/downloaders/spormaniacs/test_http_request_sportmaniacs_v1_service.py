import unittest
from unittest.mock import patch, MagicMock
from requests import RequestException
from app.infrastructure.downloader_services.spormaniacs.http_request_spormaniacs_v1_service import HttpRequestSportmaniacsV1Service
from app.infrastructure.exceptions import InvalidRaceIdException, InvalidResponseException, HttpRequestException


class TestHttpRequestSportmaniacsV1Service(unittest.TestCase):
    def setUp(self):
        self.requests_mock = MagicMock()
        self.http_service = HttpRequestSportmaniacsV1Service(self.requests_mock)

    def test_request_data_success(self):
        mock_response = MagicMock()
        expected_url = 'https://sportmaniacs.com/es/races/rankings/123e4567-e89b-12d3-a456-426614174000'
        mock_response.json.return_value = {
            'data': {
                'Rankings': [{'name': 'Runner1', 'club': 'Club1'}]
            }
        }
        self.requests_mock.get.return_value = mock_response

        url = 'https://someurl.com/123e4567-e89b-12d3-a456-426614174000'
        response = self.http_service.request_data(url)

        self.requests_mock.get.assert_called_once_with(expected_url, timeout=60)
        self.assertIn('data', response)
        self.assertIn('Rankings', response['data'])

    def test_request_data_invalid_race_id(self):
        url = 'https://someurl.com/no-race-id'
        with self.assertRaises(InvalidRaceIdException):
            self.http_service.request_data(url)

    def test_request_data_no_data(self):
        mock_response = MagicMock()
        expected_url = 'https://sportmaniacs.com/es/races/rankings/123e4567-e89b-12d3-a456-426614174000'
        mock_response.json.return_value = {}
        self.requests_mock.get.return_value = mock_response

        url = 'https://someurl.com/123e4567-e89b-12d3-a456-426614174000'
        with self.assertRaises(InvalidResponseException):
            self.http_service.request_data(url)

    def test_request_data_no_rankings(self):
        mock_response = MagicMock()
        expected_url = 'https://sportmaniacs.com/es/races/rankings/123e4567-e89b-12d3-a456-426614174000'
        mock_response.json.return_value = {'data': {}}
        self.requests_mock.get.return_value = mock_response

        url = 'https://someurl.com/123e4567-e89b-12d3-a456-426614174000'
        with self.assertRaises(InvalidResponseException):
            self.http_service.request_data(url)

    def test_request_data_requests_exception(self):
        self.requests_mock.get.side_effect = RequestException

        url = 'https://someurl.com/123e4567-e89b-12d3-a456-426614174000'
        with self.assertRaises(HttpRequestException):
            self.http_service.request_data(url)

if __name__ == '__main__':
    unittest.main()
