import json
from collections import namedtuple

import requests
from allure.constants import AttachmentType
from nose.tools import assert_in

from constants import Method
from settings import Settings
from utils import attach

HOST = Settings.BASE_URL
HEADERS = {'Content-Type': 'application/json'}
REST_PREFIX = '- REST       |'
STATUS_CODES = {Method.GET:    [200, 400, 404],
                Method.POST:   [200, 400, 404],
                Method.PUT:    [200, 400, 404],
                Method.DELETE: [201, 400, 404]}


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
            content = json.loads(response.content, object_hook=lambda d: namedtuple('Rest', d.keys())(*d.values()))
        except:
            content = response.content

        return content, response.status_code

    @classmethod
    def _send(cls, method, url, data):
        headers = HEADERS
        attach_json(f'{method.upper()} | {url}', data)

        if method in [Method.PUT, Method.DELETE]:
            headers.update(cls._get_token())

        response = {method == Method.GET:     requests.get(url, headers=headers),
                    method == Method.POST:    requests.post(url, data, headers=headers),
                    method == Method.PUT:     requests.put(url, data, headers=headers),
                    method == Method.DELETE:  requests.delete(url, headers=headers)}[True]

        assert_in(response.status_code, STATUS_CODES[method], f'Invalid Status Code: {response.status_code}\n{response.content}')
        attach_json(f'RESPONSE', response.content)

        return response


def attach_json(name, data):
    try:
        attach(name, json.dumps(json.loads(data), indent=4, sort_keys=True) if data else 'Empty body', AttachmentType.JSON)
    except:
        attach(name, data, AttachmentType.JSON)


