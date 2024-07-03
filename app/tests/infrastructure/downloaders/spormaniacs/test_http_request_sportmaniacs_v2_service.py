import unittest
from unittest.mock import patch, MagicMock
from requests import RequestException, Timeout
from app.infrastructure.downloader_services.spormaniacs.http_request_spormaniacs_v2_service import HttpRequestSportmaniacsV2Service
from app.infrastructure.exceptions import InvalidRaceIdException, InvalidResponseException, HttpRequestException, TimeoutException

class TestHttpRequestSportmaniacsV2Service(unittest.TestCase):
    def setUp(self):
        self.requests_mock = MagicMock()
        self.http_service = HttpRequestSportmaniacsV2Service(self.requests_mock)

    @patch('app.infrastructure.http_request_service.requests.get')
    def test_request_data_success(self, mock_get):
        mock_html_response = MagicMock()
        mock_html_response.text = '<html>competitionId: "123e4567-e89b-12d3-a456-426614174000"</html>'
        mock_json_response = MagicMock()
        mock_json_response.json.return_value = {'runners': [{'name': 'Runner1', 'club': 'Club1'}]}
        mock_get.side_effect = [mock_html_response, mock_json_response]

        url = 'https://someurl.com/event'
        response = self.http_service.request_data(url)

        self.assertIn('runners', response)
        self.assertEqual(response['runners'][0]['name'], 'Runner1')

    @patch('app.infrastructure.http_request_service.requests.get')
    def test_request_data_invalid_race_id(self, mock_get):
        mock_html_response = MagicMock()
        mock_html_response.text = '<html>No competition ID here</html>'
        mock_get.return_value = mock_html_response

        url = 'https://someurl.com/event'
        with self.assertRaises(InvalidRaceIdException):
            self.http_service.request_data(url)

    @patch('app.infrastructure.http_request_service.requests.get')
    def test_request_data_http_exception(self, mock_get):
        mock_get.side_effect = RequestException

        url = 'https://someurl.com/event'
        with self.assertRaises(HttpRequestException):
            self.http_service.request_data(url)

    @patch('app.infrastructure.http_request_service.requests.get')
    def test_request_data_timeout_exception(self, mock_get):
        mock_get.side_effect = Timeout

        url = 'https://someurl.com/event'
        with self.assertRaises(TimeoutException):
            self.http_service.request_data(url)

    @patch('app.infrastructure.http_request_service.requests.get')
    def test_get_competition_id_success(self, mock_get):
        mock_html_response = MagicMock()
        mock_html_response.text = '<html>competitionId: "123e4567-e89b-12d3-a456-426614174000"</html>'
        mock_get.return_value = mock_html_response

        url = 'https://someurl.com/event'
        competition_id = self.http_service._HttpRequestSportmaniacsV2Service__get_competition_id(url)

        self.assertEqual(competition_id, '123e4567-e89b-12d3-a456-426614174000')

    @patch('app.infrastructure.http_request_service.requests.get')
    def test_get_competition_id_not_found(self, mock_get):
        mock_html_response = MagicMock()
        mock_html_response.text = '<html>No competition ID here</html>'
        mock_get.return_value = mock_html_response

        url = 'https://someurl.com/event'
        competition_id = self.http_service._HttpRequestSportmaniacsV2Service__get_competition_id(url)

        self.assertIsNone(competition_id)

    @patch('app.infrastructure.http_request_service.requests.get')
    def test_get_competition_id_http_exception(self, mock_get):
        mock_get.side_effect = RequestException

        url = 'https://someurl.com/event'
        with self.assertRaises(HttpRequestException):
            self.http_service._HttpRequestSportmaniacsV2Service__get_competition_id(url)

if __name__ == '__main__':
    unittest.main()
