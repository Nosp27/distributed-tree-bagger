import asyncio
import json
from typing import Any, Dict
import requests
from .abc import Microservice
from flask import request
from threading import Event


class MasterNode(Microservice):
    def __init__(self, **kwargs):
        super().__init__()
        self.health = []
        self.health_check_event = Event()
        self.nodes = []

    def endpoint_register(self) -> Dict[str, Any]:
        self.nodes.append({'type': request.args['type'], 'host': 'http://' + request.args['address']})
        return {'status': 'registered'}

    def endpoint_resolve(self) -> Dict[str, Any]:
        ms_type = request.args['type']
        n = int(request.args.get('n', 0))
        ret_list = [{'host': h['host']} for h in self.nodes if h[0] == ms_type]
        if n:
            ret_list = ret_list[:n]
        return {'nodes': ret_list}

    def endpoint_all(self):
        return {'nodes': self.nodes}

    def endpoint_healthy(self):
        final_nodes = []
        for node in self.nodes:
            try:
                resp = requests.get(node['host'] + '/check')
                if resp.status_code == 200 and resp.json()['status'] == 'healthy':
                    final_nodes.append(node)
            except:
                pass

        return {'healthy_nodes': final_nodes}


def endpoint_health(self) -> Dict[str, Any]:
    self.health_check_event.wait()
    return {'health': self.health}


async def hc(self):
    while True:
        self.health_check_event.set()
        for _, host in self.nodes:
            try:
                x = json.loads(requests.get('%s/%s' % (host, 'check')), timeout=0.1)['status']
            except Exception:
                x = None
            self.health[host] = x
        self.health_check_event.clear()
        await asyncio.sleep(5)
