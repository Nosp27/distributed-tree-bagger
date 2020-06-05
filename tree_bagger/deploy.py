import json
import os
import requests
from time import sleep


def deploy(*, sleep_time=2):
    os.environ['master_node'] = 'http://localhost:8080'
    with open('deploy.json') as f:
        config = json.loads(f.read())

    try:
        assert requests.get(os.environ['master_node'] + '/check').status_code != 200
    except (requests.exceptions.ConnectionError, AssertionError):
        os.system(f'nohup python -m tree_bagger 8080 > out_master.log &')

    for service in config:
        port = service['port']
        os.system(f'nohup python -m tree_bagger {port} > out{port}.log &')

    sleep(sleep_time)

    requests.get(os.environ['master_node'] + '/deploy?type=MasterNode&port=8080').raise_for_status()

    for service in config:
        resp = requests.get('http://localhost:%s/deploy?port=%s&type=%s' % (
            service['port'], service['port'], service['microservice_cls']
        ))
        resp.raise_for_status()
        assert json.loads(resp.content)['status'] == 'deployed'


def stop():
    with open('deploy.json') as f:
        config = json.loads(f.read())
    for service in config:
        try:
            requests.get('http://localhost:%s/kill' % service['port'])
        except:
            pass

    try:
        requests.get('%s/kill' % os.environ['master_node'])
    except:
        pass
