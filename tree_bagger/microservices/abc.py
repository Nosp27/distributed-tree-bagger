import json
import logging
import os
import flask
import requests


class Microservice:
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
        logging.debug('Recieved: %s' % flask.request.data)
        return json.loads(flask.request.data)

    def load_queryargs(self):
        logging.debug('Recieved Queryargs: %s' % flask.request.args)
        return flask.request.args

    def get_nodes_of_type(self, node_type, n=0):
        resp = requests.get(
                '%s/microservice/%s?type=%s&n=%s' % (os.environ['master_node'], 'endpoint_resolve', node_type, n), timeout=0.1
            )
        resp.raise_for_status()
        return json.loads(
            resp.content
        )['nodes']
