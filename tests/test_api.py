import json


def test_deployment(test_client):
    response = test_client.get('/deploy')
    assert response.status_code == 200
    deploy_get = response.json
    assert deploy_get['status'] == 'deployed'


def test_deploy_with_config(test_client):
    response = test_client.post('/deploy', data={'config': {"microservice_cls": "RandomForestMicroservice"}})
    assert response.status_code == 200


def test_fit(test_client):
    response = test_client.post('/deploy', data={'config': {"microservice_cls": "RandomForestMicroservice"}})
    assert response.status_code == 200

    fit_response = test_client.post('/microservice/endpoint_fit', data={
        'command': 'fit',
        'config': {'max_depth': 3},
        'X': [[1,2,3], [1,3,4]],
        'y': [1, 0],
    })

    assert fit_response.status_code == 200

    assert fit_response['status'] == 'done'
    assert fit_response['accuracy'] > 0.2
