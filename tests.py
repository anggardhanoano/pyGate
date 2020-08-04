from falcon import testing
import falcon
import json
import jwt
import pytest
import requests

from gateway.constant import JWT_SETTINGS
import server


@pytest.fixture
def client():
    app, _ = server.create_server('service_test.json')
    return testing.TestClient(app)

# pytest will inject the object returned by the "client" function
# as an additional parameter.
def test_url_public(client):

    BODY = json.dumps({
        "halo": "haha"
    })

    response = client.simulate_get('/testing/get')
    assert response.status == falcon.HTTP_OK

    response = client.simulate_post(
        '/testing/post',
        body = BODY
        )
    assert response.status == falcon.HTTP_OK
    
    response = client.simulate_put(
        '/testing/put',
        body = BODY
    )
    assert response.status == falcon.HTTP_OK

    response = client.simulate_patch(
        '/testing/patch',
        body = BODY
    )
    assert response.status == falcon.HTTP_OK

    response = client.simulate_delete('/testing/delete')
    assert response.status == falcon.HTTP_OK

    response = client.simulate_get('/testing/param/200')
    assert response.status == falcon.HTTP_OK

    response = client.simulate_get('/testing/hahaha')
    assert response.status == falcon.HTTP_404

    response = client.simulate_get('/local/post')
    assert response.status == falcon.HTTP_504

    response = client.simulate_get('/local/hai')
    assert response.status == falcon.HTTP_508


def test_url_private(client):

    jwt_token = jwt.encode({"haha": "hehe"}, JWT_SETTINGS["JWT_KEY"], algorithm='HS256').decode("utf-8")
    headers = {
        'Authorization': 'JWT ' + jwt_token
    }

    response = client.simulate_get('/testing-private/get')
    assert response.status == falcon.HTTP_401

    response = client.simulate_get('/testing-private/get', headers=headers)
    assert response.status == falcon.HTTP_OK

    response = client.simulate_post('/testing-private/post', body=json.dumps({"haha":"hehe"}), headers=headers)
    assert response.status == falcon.HTTP_OK

    response = client.simulate_post('/testing-private/post?q=hehe', body=json.dumps({"haha":"hehe"}), headers=headers)
    assert response.status == falcon.HTTP_OK

    jwt_token = jwt.encode({"haha": "hehe"}, "haihai", algorithm='HS256').decode("utf-8")
    headers = {
        'Authorization': 'JWT ' + jwt_token
    }

    response = client.simulate_get('/testing-private/get', headers=headers)
    assert response.status == falcon.HTTP_401