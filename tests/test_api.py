import tree_bagger
import requests


def test_deployment():
    # tree_bagger.start()
    response = requests.get('/deploy')
    response.raise_for_status()
    deploy_get = response.json()
    assert deploy_get['status'] == 'deployed'
