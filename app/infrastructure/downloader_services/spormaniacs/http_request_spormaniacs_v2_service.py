import logging
import re
import requests
from app.domain.repository.idownloader_service import IHttpRequestService


class HttpRequestSportmaniacsV2Service(IHttpRequestService):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def request_data(self, url: str) -> dict:
        competition_id = self.__get_competition_id(url)
        
        url = f'https://rankings-storage.timingsense.cloud/prod/competitions/{competition_id}/Carrera%20(Modalidad%20competitiva)/participants.json'
        
        runners = requests.get(url, timeout=60).json()

        return runners

    def __get_competition_id(self, url):
        if '/rankings' not in url:
            url = url + '/rankings'

        html = requests.get(url, timeout=60).text
        regex = r'competitionId: "([a-f0-9-]+)"'
        matches = re.findall(regex, html)
        return matches[0]
