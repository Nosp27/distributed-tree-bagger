import abc
import pickle
from symbol import decorator
from typing import Dict
import asyncio


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
