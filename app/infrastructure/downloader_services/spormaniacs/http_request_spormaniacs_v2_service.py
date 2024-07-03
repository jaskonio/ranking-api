import logging
import re
import requests
from app.domain.repository.idownloader_service import IHttpRequestService
from app.infrastructure.exceptions import HttpRequestException, InvalidRaceIdException, TimeoutException


class HttpRequestSportmaniacsV2Service(IHttpRequestService):
    def __init__(self, requests:requests):
        self.logger = logging.getLogger(__name__)
        self.requests = requests

    def request_data(self, url: str) -> dict:
        competition_id = self.__get_competition_id(url)

        if competition_id is None:
            self.logger.error(f'Invalid race ID in URL: {url}')
            raise InvalidRaceIdException(f'Invalid race ID in URL: {url}')   

        try:
            url = f'https://rankings-storage.timingsense.cloud/prod/competitions/{competition_id}/Carrera%20(Modalidad%20competitiva)/participants.json'
            response = self.requests.get(url, timeout=60)
            response.raise_for_status()  # Raises HTTPError for bad responses
            runners = response.json()
        
        except requests.Timeout as e:
            self.logger.error(f'HTTP request timed out: {e}')
            raise TimeoutException(f'HTTP request timed out: {e}')
        except requests.RequestException as e:
            self.logger.error(f'HTTP request failed: {e}')
            raise HttpRequestException(f'HTTP request failed: {e}')

        return runners

    def __get_competition_id(self, url):
        if '/rankings' not in url:
            url = url + '/rankings'

        try:
            html = self.requests.get(url, timeout=60).text
        except requests.RequestException as e:
            self.logger.error(f'Failed to fetch HTML page: {e}')
            raise HttpRequestException(f'Failed to fetch HTML page: {e}')
        
        regex = r'competitionId: "([a-f0-9-]+)"'
        matches = re.findall(regex, html)
        return matches[0] if matches else None
