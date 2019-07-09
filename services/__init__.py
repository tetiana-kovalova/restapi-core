import json
import time
from collections import namedtuple

import requests
from allure.constants import AttachmentType
from nose.tools import assert_in

from constants import Service
from settings import Settings
from utils import attach

HEADERS = Settings.HEADERS
REST_PREFIX = '- REST       |'
STATUS_CODES = {Service.GET:    [200, 400, 404],
                Service.POST:   [200, 400, 404],
                Service.PUT:    [200, 400, 404],
                Service.DELETE: [201, 400, 404]}


class Rest(object):

    @classmethod
    def service(cls, service, route, data=None):
        host = Settings.BASE_URL

        url = f'{host}/{route}'

        try:
            response = cls._service(service, url, data=json.dumps(data) if data else None)
        except AssertionError:
            time.sleep(1)
            response = cls._service(service, url, data=json.dumps(data) if data else None)

        if len(response.json()) == 1:
            content = []

            for item in response.json()['1']:
                content.append(json.loads(json.dumps(item), object_hook=lambda d: namedtuple('Rest', d.keys())(*d.values())))
        else:
            content = json.loads(response.content, object_hook=lambda d: namedtuple('Rest', d.keys())(*d.values()))

        status_code = response.status_code

        return content, status_code

    @classmethod
    def _service(cls, service, url, data):
        attach_json(f'{service.upper()} | {url}', data if data else '{"message": "Body is empty"}')

        response = {service == Service.GET:     requests.get(url,        headers=HEADERS),
                    service == Service.POST:    requests.post(url, data, headers=HEADERS),
                    service == Service.PUT:     requests.put(url, data,  headers=HEADERS),
                    service == Service.DELETE:  requests.delete(url,     headers=HEADERS)}[True]

        assert_in(response.status_code, STATUS_CODES[service],
                  f'Invalid Status Code: {response.status_code}\n{response.content}')

        attach_json(f'RESPONSE', response.content)

        return response


def attach_json(name, data):
    attach(name, json.dumps(json.loads(data), indent=4, sort_keys=True), AttachmentType.JSON)
