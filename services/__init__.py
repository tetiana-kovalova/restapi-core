import json
import time
from collections import namedtuple

import requests
from allure.constants import AttachmentType
from nose.tools import assert_in

from constants import Service
from settings import Settings
from utils import attach

HOST = Settings.BASE_URL
HEADERS = {'Content-Type': 'application/json'}
REST_PREFIX = '- REST       |'
STATUS_CODES = {Service.GET:    [200, 400, 404],
                Service.POST:   [200, 400, 404],
                Service.PUT:    [200, 400, 404],
                Service.DELETE: [201, 400, 404]}


class Rest(object):
    @classmethod
    def _get_token(cls):
        route = 'auth'
        url = f'{HOST}/{route}'

        response = requests.post(url, '{"username": "admin", "password": "password123"}', headers=HEADERS).json()

        return {'Cookie': f'token={response["token"]}'}

    @classmethod
    def service(cls, service, route, data=None):
        url = f'{HOST}/{route}'

        try:
            response = cls._service(service, url, data=json.dumps(data) if data else None)
        except AssertionError:
            time.sleep(1)
            response = cls._service(service, url, data=json.dumps(data) if data else None)

        try:
            content = json.loads(response.content, object_hook=lambda d: namedtuple('Rest', d.keys())(*d.values()))
        except:
            content = response.content

        status_code = response.status_code

        return content, status_code

    @classmethod
    def _service(cls, service, url, data):
        headers = HEADERS
        attach_json(f'{service.upper()} | {url}', data if data else '{"message": "Body is empty"}')

        if service in [Service.PUT, Service.DELETE]:
            headers.update(cls._get_token())

        response = {service == Service.GET:     requests.get(url, headers=headers),
                    service == Service.POST:    requests.post(url, data, headers=headers),
                    service == Service.PUT:     requests.put(url, data, headers=headers),
                    service == Service.DELETE:  requests.delete(url, headers=headers)}[True]

        assert_in(response.status_code, STATUS_CODES[service], f'Invalid Status Code: {response.status_code}\n{response.content}')
        attach_json(f'RESPONSE', response.content)

        return response


def attach_json(name, data):
    try:
        attach(name, json.dumps(json.loads(data), indent=4, sort_keys=True), AttachmentType.JSON)
    except:
        attach(name, data, AttachmentType.TEXT)


