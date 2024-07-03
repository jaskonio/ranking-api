import logging
import re
import requests
from app.domain.repository.idownloader_service import IHttpRequestService
from app.infrastructure.exceptions import HttpRequestException, InvalidRaceIdException, InvalidResponseException


class HttpRequestSportmaniacsV1Service(IHttpRequestService):
    def __init__(self, requests: requests):
        self.logger = logging.getLogger(__name__)
        self.requests = requests

    def request_data(self, url: str) -> dict:
        race_id = self._extract_race_id(url)

        if race_id is None:
            self.logger.error(f'Invalid race ID in URL: {url}')
            raise InvalidRaceIdException(f'Invalid race ID in URL: {url}')   

        try:
            url = 'https://sportmaniacs.com/es/races/rankings/' + race_id
            response = self.requests.get(url, timeout=60)
            response_json = response.json()
        except requests.RequestException as e:
            self.logger.error(f'HTTP request failed: {e}')
            raise HttpRequestException(f'HTTP request failed: {e}')

        if 'data' not in response_json or 'Rankings' not in response_json['data']:
            self.logger.error(f'Invalid response structure: {response_json}')
            raise InvalidResponseException(f'Invalid response structure: {response_json}')

        return response_json

    def _extract_race_id(self, url: str) -> str:
        pattern = r'([a-f0-9-]{36})'
        match = re.search(pattern, url)
        return match.group(0) if match else None