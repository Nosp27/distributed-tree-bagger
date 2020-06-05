import json
from typing import Any, Dict
import logging

import numpy as np
import requests

from .abc import Microservice


class SplitterMicroservice(Microservice):
    def __init__(self):
        super().__init__()
        self._endpoints = []

    def endpoint_split(self) -> Dict[str, Any]:
        data = self.load_data()
        assert data['command'] == 'fit'

        X = np.array(data['X'])

        n_features = data.get('n_features', X.shape[1] // 3 + 1)
        n_trees = data.get('n_trees', 3)
        n_samples = data.get('n_samples', X.shape[0])

        children = self.get_nodes_of_type('RandomForestMicroservice', n_trees)
        if n_trees > len(children):
            n_trees = len(children)
            # TODO: send alerts

        assert X.shape[1] >= n_features

        split = [np.random.choice(X.shape[1] - 1, n_features, replace=False).tolist() for _ in range(n_trees)]
        samples = [np.random.choice(X.shape[0], n_samples) for _ in range(n_trees)]

        if data.get('inplace'):
            return {'split': split}

        logging.debug(children)

        responses = [
            requests.post('%s/microservice/endpoint_fit' % (child['host']),
                          data=json.dumps(self.form_fit_data(one_split, one_sample)),
                          headers={'Content-Type': 'application/json'})
            for one_split, one_sample, child in zip(split, samples, children)
        ]

        logging.debug(responses)

        for r in responses:
            r.raise_for_status()

        return {'responses': [r.json() for r in responses]}

    def form_fit_data(self, split, samples) -> Dict[str, Any]:
        data = self.load_data()
        X = np.array(data['X'])
        y = np.array(data['y'])

        logging.debug('samples: %s, split: %s' % (samples, split))

        sended_data = {
            'config': data['config'],
            'command': 'fit',
            'X': X[samples][:, split].tolist(),
            'y': y[samples].tolist(),
        }

        if 'model_name' in data:
            sended_data['model_name'] = data['model_name']

        logging.debug('sending: %s' % sended_data)

        return sended_data
