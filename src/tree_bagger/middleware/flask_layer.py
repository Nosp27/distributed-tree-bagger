from typing import Any, Dict, List
import logging
import flask


class FlaskLayer:
    def __init__(self, endpoints: List[Dict[str, Any]]):
        logging.basicConfig(level='DEBUG')
        self.logger = logging.getLogger(self.__class__.__name__)
        self.app = flask.Flask(__name__)

        for endpoint in endpoints:
            url = '/microservice%s' % endpoint['url']
            self.app.add_url_rule(url, endpoint['name'], endpoint['func'], methods=['GET', 'POST'])
            self.logger.info('Added handler %s at %s' % (url, endpoint['name']))
