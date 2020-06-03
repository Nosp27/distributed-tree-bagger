from typing import Any, Dict

from .abc import Microservice


class BaggerMicroservice(Microservice):
    def __init__(self):
        super().__init__()
        self._endpoints = []

    def endpoint_bag(self) -> Dict[str, Any]:
        data = self.load_data()
        assert data['command'] == 'bag'

        predicts = data['predicts']
        bagged_result = sum(predicts) / len(predicts)

        return {'result': bagged_result}
