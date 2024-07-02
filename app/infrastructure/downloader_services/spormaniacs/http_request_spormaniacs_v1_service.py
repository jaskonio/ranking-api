import logging
import re
import requests
from app.domain.repository.idownloader_service import IHttpRequestService


class HttpRequestSportmaniacsV1Service(IHttpRequestService):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def request_data(self, url: str) -> dict:
        race_id = 'None'

        pattern = r'([a-f0-9-]{36})'
        match = re.search(pattern, url)
        if match:
            race_id = match.group(0)

        url = 'https://sportmaniacs.com/es/races/rankings/' + race_id
        response = requests.get(url, timeout=60)
        response_json = response.json()

        if 'data' not in response_json or 'Rankings' not in response_json['data']:
            return []

        return response_json