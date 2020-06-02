import json
import pickle
from typing import Any, Dict
import numpy as np

import flask

from .abc import Microservice
from sklearn.tree import DecisionTreeClassifier


class RandomForestMicroservice(Microservice):
    def __init__(self):
        super().__init__()
        self._endpoints = []

    def endpoint_fit(self) -> Dict[str, Any]:
        data = json.loads(flask.request.data.decode())
        if data['command'] != 'fit':
            raise ValueError('Command fit is not in config')

        clf = DecisionTreeClassifier(**data.get('config', {}))
        clf.fit(np.array(data['train']), np.array(data['test']))

        self.save(clf)
        return {'status': 'done'}

    def endpoint_predict(self, data: Dict[str, Any]):
        if data['command'] != 'predict':
            raise ValueError('Command predict is not in config')
        clf = self.load()
        return clf.predict(data['matrix'])

    def save(self, model):
        with open('./data/clf.pkl', 'wb') as f:
            pickle.dump(model, f)

    def load(self):
        with open('./data/clf.pkl', 'r') as f:
            return pickle.load(f)





