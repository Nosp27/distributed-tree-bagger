import pickle
from typing import Any, Dict
import numpy as np

from .abc import Microservice
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


class RandomForestMicroservice(Microservice):
    def __init__(self):
        super().__init__()
        self._endpoints = []

    def endpoint_fit(self) -> Dict[str, Any]:
        data = self.load_data()
        if data['command'] != 'fit':
            raise ValueError('Command fit is not in config')

        clf = DecisionTreeClassifier(**data.get('config', {}))
        clf.fit(np.array(data['X']), np.array(data['y']))

        self.save(clf)
        return {'status': 'done', 'accuracy': accuracy_score(np.array(data['y']), clf.predict(data['X']))}

    def endpoint_predict(self):
        data = self.load_data()
        if data['command'] != 'predict':
            raise ValueError('Command predict is not in config')
        clf = self.load()
        return {'predict': clf.predict(data['data']).tolist()}

    def save(self, model):
        with open('./data/clf.pkl', 'wb') as f:
            pickle.dump(model, f)

    def load(self):
        with open('./data/clf.pkl', 'rb') as f:
            return pickle.load(f)





