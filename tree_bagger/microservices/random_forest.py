import json
import logging
import pickle
from typing import Any, Dict
import numpy as np

from .abc import Microservice
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


class RandomForestMicroservice(Microservice):
    def __init__(self, **kwargs):
        super().__init__()
        self._endpoints = []
        self.port = kwargs.pop('port')

    def endpoint_fit(self) -> Dict[str, Any]:
        data = self.load_data()

        if data['command'] != 'fit':
            raise ValueError('Command fit is not in config')

        clf = DecisionTreeClassifier(**data.get('config', {}))
        clf.fit(np.array(data['X']), np.array(data['y']))

        self.save(clf, data['features'], data.get('model_name'))
        return {'status': 'done', 'accuracy': accuracy_score(np.array(data['y']), clf.predict(data['X']))}

    def endpoint_predict(self):
        data = self.load_data()
        if data['command'] != 'predict':
            raise ValueError('Command predict is not in config')
        clf = self.load(data.get('model_name'))
        return {'predict': clf.predict(data['data']).tolist()}

    def endpoint_features(self):
        data = self.load_queryargs()
        return {'features': self.load_features(data.get('model_name'))}

    def save(self, model, features, model_name='clf'):
        model_name = model_name or 'clf'
        with open('./data/%s_%s.pkl' % (model_name, self.port), 'wb') as f:
            pickle.dump(model, f)
        with open('./data/%s_%s.features' % (model_name, self.port), 'w') as f:
            json.dump(features, f)

    def load(self, model_name=None):
        model_name = model_name or 'clf'
        with open('./data/%s_%s.pkl' % (model_name, self.port), 'rb') as f:
            return pickle.load(f)

    def load_features(self, model_name=None):
        model_name = model_name or 'clf'
        with open('./data/%s_%s.features' % (model_name, self.port), 'rb') as f:
            return json.load(f)
