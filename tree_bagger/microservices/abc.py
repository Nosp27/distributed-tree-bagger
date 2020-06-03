import json
from typing import Dict

import flask


class Microservice:
    def __init__(self, dependencies: Dict[str, str] = None):
        self.dependencies = dependencies or {}

    def get_endpoints(self):
        endpoints = [attr for attr in dir(self) if attr.startswith('endpoint')]
        return [
            {
                'url': "/%s/%s" % (self.__class__.__name__, attr),
                'name': attr,
                'func': getattr(self, attr)
            }
            for attr in endpoints
        ]

    def load_data(self):
        return json.loads(flask.request.data.decode())
