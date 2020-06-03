from typing import Any, Dict

import numpy as np
import requests

from .abc import Microservice


class SplitterMicroservice(Microservice):
    def __init__(self, children=None):
        super().__init__()
        self._endpoints = []
        self._children = children or []

    def endpoint_split(self) -> Dict[str, Any]:
        data = self.load_data()
        assert data['command'] == 'fit'

        X = np.array(data['X'])

        n_features = data.get('n_feautres', X.shape[1] / 3 + 1)
        n_trees = data.get('n_trees', 3)
        n_samples = data.get('n_samples', X.shape[0])

        if n_trees > len(self._children):
            n_trees = len(self._children)
            # TODO: send alerts

        assert X.shape[1] >= n_features

        split = [np.random.choice(X.shape[1], n_features, replace=False).aslist() for _ in n_trees]
        samples = [np.random.choice(X.shape[0], n_samples) for _ in n_trees]

        if not self._children:
            return {'split': split}

        responses = [
            requests.post(child, self.form_fit_data(s, samples))
            for s, child in zip(split, self._children)
        ]

        return {'responses': responses}

    def form_fit_data(self, split, samples) -> Dict[str, Any]:
        data = self.load_data()
        X = np.array(data['X'])
        y = np.array(data['y'])

        return {
            'config': data['config'],
            'command': 'fit',
            'X': X[samples, split],
            'y': y[samples],
        }
