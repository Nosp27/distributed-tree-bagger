import json
import os

import waitress as waitress

from tree_bagger.microservices.abc import Microservice
from tree_bagger.microservices.random_forest import RandomForestMicroservice
from tree_bagger.middleware.flask_layer import FlaskLayer

if __name__ == '__main__':
    print(os.system('pwd'))
    with open('../../deploy.json', 'r') as config_file:
        config = json.load(config_file)
    microservice_cls, *_ = [x for x in Microservice.__subclasses__() if x.__name__ == config['microservice_cls']]
    microservice_instance = microservice_cls()
    flask_layer = FlaskLayer(microservice_instance.get_endpoints())
    waitress.serve(flask_layer.app)
