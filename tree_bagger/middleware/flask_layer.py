import json
import logging
import requests
import flask
import os
from werkzeug import exceptions

from tree_bagger import Microservice


class FlaskLayer:
    def __init__(self, *, config=None):
        import os
        os.system('pwd')
        logging.basicConfig(level='DEBUG')
        self.logger = logging.getLogger(self.__class__.__name__)
        self.app = flask.Flask(__name__)

        self.endpoints = {}
        self.master_node = None
        self.config = config or 'deploy.json'

        self.app.add_url_rule('/deploy', 'deploy', self.deploy, methods=['GET', 'POST'])
        self.app.add_url_rule('/kill', 'kill', self.kill, methods=['GET'])
        self.app.add_url_rule('/check', 'check', self.check)
        self.app.add_url_rule(
            '/microservice/<string:name>',
            'serve_microservice',
            self.serve_microservice, methods=['GET', 'POST']
        )

    def deploy(self):
        if self.endpoints:
            return {'status': 'already deployed'}

        self.master_node = os.environ['master_node']
        cls_name = flask.request.args['type']
        print(cls_name)
        self.logger.debug(cls_name)
        microservice_cls = [c for c in Microservice.__subclasses__() if c.__name__ == cls_name][0]

        microservice_instance = microservice_cls()
        if cls_name != 'MasterNode':
            resp = requests.get('%s/%s?type=%s&address=%s' % (
                self.master_node, 'microservice/endpoint_register', microservice_cls.__name__, flask.request.host
            ))
            resp.raise_for_status()
            assert json.loads(resp.content)['status'] == 'registered'
        self.logger.info('Added microservice %s' % microservice_cls.__name__)

        self.endpoints = {
            e['name']: e for e in microservice_instance.get_endpoints()
        }

        for name in self.endpoints.keys():
            self.logger.info('Added %s' % name)

        return {'status': 'deployed', 'type': microservice_cls.__name__}

    def check(self):
        if not self.endpoints:
            return {'status': 'not deployed'}
        return {'status': 'healthy'}

    def serve_microservice(self, name):
        if not self.endpoints:
            raise exceptions.PreconditionFailed('Not deployed yed!')
        try:
            return self.endpoints[name]['func']()
        except Exception as e:
            logging.exception('EXC!', exc_info=e)
            return exceptions.InternalServerError('\n'.join(e.args))

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

    def kill(self):
        return os.system('kill %s' % os.getpid())
