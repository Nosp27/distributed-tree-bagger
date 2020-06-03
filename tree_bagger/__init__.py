import waitress as waitress

from tree_bagger.microservices.abc import Microservice
from tree_bagger.microservices.random_forest import RandomForestMicroservice
from tree_bagger.middleware.flask_layer import FlaskLayer


def start():
    flask_layer = FlaskLayer()
    waitress.serve(flask_layer.app)


__all__ = ['start']


if __name__ == "__main__":
    start()
