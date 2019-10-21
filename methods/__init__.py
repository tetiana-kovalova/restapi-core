import json
import requests

from constants import Method
from settings import Settings
from utils.logger import BaseLogger


HOST = Settings.BASE_URL
HEADERS = {'Content-Type': 'application/json'}

logger = BaseLogger()


class Rest(object):
    @classmethod
    def _get_token(cls):
        route = 'auth'
        url = f'{HOST}/{route}'

        response = requests.post(url, '{"username": "admin", "password": "password123"}', headers=HEADERS).json()

        return {'Cookie': f'token={response["token"]}'}

    @classmethod
    def send(cls, service, route, data=None):
        url = f'{HOST}/{route}'

        response = cls._send(service, url, data=json.dumps(data) if data else None)

        try:
            content = response.json()
        except:
            content = response.content

        return content, response.status_code

    @classmethod
    def _send(cls, method, url, data):
        headers = HEADERS
        logger.info(f'REQUEST - {method.upper()}: [{url}] with payload [{data}]')

        if method in [Method.PUT, Method.DELETE]:
            headers.update(cls._get_token())

        response = {method == Method.GET:     requests.get(url, headers=headers),
                    method == Method.POST:    requests.post(url, data, headers=headers),
                    method == Method.PUT:     requests.put(url, data, headers=headers),
                    method == Method.DELETE:  requests.delete(url, headers=headers)}[True]

        assert response.status_code <= 404, f'Invalid Status Code: {response.status_code}\n{response.content}'
        logger.info(f'RESPONSE - {response.status_code}: [{response.content}]')

        return response
