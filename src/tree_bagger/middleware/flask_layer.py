import json
from typing import Any, Dict, List
import logging
import flask
from werkzeug import exceptions

from tree_bagger import Microservice


class FlaskLayer:
    def __init__(self):
        logging.basicConfig(level='DEBUG')
        self.logger = logging.getLogger(self.__class__.__name__)
        self.app = flask.Flask(__name__)

        self.endpoints = {}

        self.app.add_url_rule('/deploy', 'deploy', self.deploy)
        self.app.add_url_rule(
            '/microservice/<string:name>/<string:endpoint>',
            'serve_microservice',
            self.serve_microservice, methods=['GET', 'POST']
        )

    def deploy(self):
        if self.endpoints:
            return {'status': 'already deployed'}

        with open('../../deploy.json', 'r') as config_file:
            config = json.load(config_file)

        microservice_cls, *_ = [
            x for x in Microservice.__subclasses__() if x.__name__ == config['microservice_cls']
        ]

        microservice_instance = microservice_cls()
        self.logger.info('Added microservice %s' % microservice_cls.__name__)

        self.endpoints = {
            e['name']: e for e in microservice_instance.get_endpoints()
        }

        for name in self.endpoints.keys():
            self.logger.info('Added %s' % name)

        return {'status': 'deployed'}

    def serve_microservice(self, name):
        if not self.endpoints:
            raise exceptions.PreconditionFailed('Not deployed yed!')
        return self.endpoints[name]['func']()
