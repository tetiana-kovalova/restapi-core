import json
import time
from collections import namedtuple

import requests
from allure.constants import AttachmentType
from nose.tools import assert_in

from constants import Service
from settings import Settings
from utils import attach

REST_PREFIX = '- REST       |'
STATUS_CODES = {Service.GET:    [200, 400, 404],
                Service.POST:   [201, 400, 404],
                Service.PUT:    [201, 400, 404],
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

    # @classmethod
    # def post(cls, service, route, data):
    #     host = Settings.BASE_URL
    #
    #     url = f'{host}/{service}/{route}'
    #
    #     try:
    #         response = cls._post(url, json.dumps(data))
    #     except AssertionError:
    #         time.sleep(1)
    #         response = cls._post(url, json.dumps(data))
    #
    #     if len(response.json()) == 1:
    #         content = []
    #
    #         for item in response.json()['1']:
    #             content.append(json.loads(json.dumps(item), object_hook=lambda d: namedtuple('Rest', d.keys())(*d.values())))
    #     else:
    #         content = json.loads(response.content, object_hook=lambda d: namedtuple('Rest', d.keys())(*d.values()))
    #
    #     status_code = response.status_code
    #
    #     return content, status_code

    @classmethod
    def _service(cls, service, url, data, headers=None):
        if data:
            attach_json(f'{service.upper()} | {url}', data)

        headers = {'Content-Type': 'application/json'} if headers is None else headers

        response = {service == Service.GET:     requests.get(url, headers=headers),
                    service == Service.POST:    requests.post(url, data, headers=headers),
                    service == Service.PUT:     requests.put(url, data, headers=headers),
                    service == Service.DELETE:  requests.delete(url, headers=headers)}[True]

        assert_in(response.status_code, STATUS_CODES[service], f'Invalid Status Code: {response.status_code}\n{response.content}')
        attach_json(f'RESPONSE', response.content)
        return response

    # @classmethod
    # def _post(cls, url, data, headers=None):
    #     attach_json(f'POST | {url}', data)
    #
    #     response = requests.post(url, data, headers={'Content-Type': 'application/json'} if headers is None else headers)
    #     assert_in(response.status_code, [201, 400, 404], f'Invalid Status Code: {response.status_code}\n{response.content}')
    #     attach_json(f'RESPONSE', response.content)
    #     return response
    #
    # @classmethod
    # def _get(cls, url, headers=None):
    #     response = requests.get(url, headers={'Content-Type': 'application/json'} if headers is None else headers)
    #     attach_json(f'GET | {url}', response)
    #
    #     assert_in(response.status_code, [200, 400, 404], f'Invalid Status Code: {response.status_code}\n{response.content}')
    #     return response


def attach_json(name, data):
    attach(name, json.dumps(json.loads(data), indent=4, sort_keys=True), AttachmentType.JSON)
