import json
import logging
import uuid
from time import time
from typing import Any, Dict

import numpy as np
import requests

from .abc import Microservice


class BaggerMicroservice(Microservice):
    def __init__(self, **kwargs):
        super().__init__()
        self.mid = uuid.UUID(bytes=str(time())[:16].encode())
        self._endpoints = []

    def endpoint_bag(self) -> Dict[str, Any]:
        data = self.load_data()
        assert data['command'] == 'predict'

        predicts = []
        children = self.get_nodes_of_type('RandomForestMicroservice')
        for child in children:
            logging.debug(f'Predicting for {child["host"]}')
            logging.debug('Loading features')
            resp = requests.get(child['host'] + (
                (
                    '/microservice/endpoint_features' +
                    '?model_name=%s' % data['model_name'] if 'model_name' in data else ''
                )
            ))
            resp.raise_for_status()
            features = resp.json()['features']
            data['features'] = features
            logging.debug(f'Features: {features}')

            data_for_predict = data.copy()
            data_for_predict['data'] = np.array(data['data'])[:, features].tolist()
            logging.debug('Prepared data: %s' % data_for_predict['data'])

            resp = requests.post(child['host'] + '/microservice/endpoint_predict', data=json.dumps(data_for_predict))
            resp.raise_for_status()
            logging.debug('Added predict')
            predicts.append(resp.json()['predict'])
            logging.debug('Parsed predict')
        predicts = np.array(predicts)
        bagged_result = predicts.mean(axis=0).round().tolist()

        return {'result': bagged_result}
