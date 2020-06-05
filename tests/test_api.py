import tree_bagger


def create_client():
    flask_app = tree_bagger.start_flask()

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()
    return testing_client, ctx


def pop_context(ctx):
    ctx.pop()


def test_deployment():
    test_client, ctx = create_client()
    response = test_client.get('/deploy')
    assert response.status_code == 200
    deploy_get = response.json
    assert deploy_get['status'] == 'deployed'
    pop_context(ctx)


def test_deploy_with_config():
    test_client, ctx = create_client()
    response = test_client.post('/deploy', data={
        'config': {
            "master_node": "http://localhost:8080", "microservice_cls": "RandomForestMicroservice"
        }
    })
    assert response.status_code == 200
    assert response.json['type'] == 'RandomForestMicroservice'
    pop_context(ctx)


def test_fit():
    test_client, ctx = create_client()
    response = test_client.post('/deploy', data={
        'config': {
            "master_node": "http://localhost:8080", "microservice_cls": "RandomForestMicroservice"
        }
    })
    assert response.status_code == 200

    fit_response = test_client.post('/microservice/endpoint_fit', data={
        'command': 'fit',
        'config': {'max_depth': 3},
        'X': [[1, 2, 3], [1, 3, 4]],
        'y': [1, 0],
    })

    assert fit_response.status_code == 200

    assert fit_response['status'] == 'done'
    assert fit_response['accuracy'] > 0.2
    pop_context(ctx)
