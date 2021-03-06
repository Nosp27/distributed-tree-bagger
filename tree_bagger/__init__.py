import waitress as waitress

from tree_bagger.microservices.abc import Microservice
from tree_bagger.microservices.random_forest import RandomForestMicroservice
from tree_bagger.middleware.flask_layer import FlaskLayer


def start_flask(config=None):
    return FlaskLayer(config=config).app


def start(*, port=8080, config=None):
    waitress.serve(start_flask(config), port=port)
