import json
import logging

import flask
from werkzeug import exceptions

from tree_bagger import Microservice


class FlaskLayer:
    def __init__(self, config=None):
        import os; os.system('pwd')
        logging.basicConfig(level='DEBUG')
        self.logger = logging.getLogger(self.__class__.__name__)
        self.app = flask.Flask(__name__)

        self.endpoints = {}
        self.config = config or 'deploy.json'

        self.app.add_url_rule('/deploy', 'deploy', self.deploy, methods=['GET', 'POST'])
        self.app.add_url_rule(
            '/microservice/<string:name>/<string:endpoint>',
            'serve_microservice',
            self.serve_microservice, methods=['GET', 'POST']
        )

    def deploy(self):
        if self.endpoints:
            return {'status': 'already deployed'}

        config = self.get_config()

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

    def get_config(self):
        try:
            self.config = json.loads(flask.request.data).get('config') or self.config
        except json.JSONDecodeError or TypeError:
            pass
        try:
            config = json.loads(self.config)
        except Exception:
            with open(self.config, 'r') as f:
                config = f.read()
        return json.loads(config)
