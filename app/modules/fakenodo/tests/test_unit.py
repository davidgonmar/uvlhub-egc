import pytest
from flask import Flask
from app.modules.fakenodo.routes import fakenodo_bp


@pytest.fixture(scope='module')
def test_client():
    app = Flask(__name__)
    app.register_blueprint(fakenodo_bp)
    with app.test_client() as client:
        with app.app_context():
            yield client


def test_test_connection_fakenodo(test_client):
    response = test_client.get('/fakenodo/api')
    assert response.status_code == 200
    assert response.json == {"status": "success", "message": "Connected to FakenodoAPI"}


def test_create_fakenodo(test_client):
    response = test_client.post('/fakenodo/api')
    assert response.status_code == 201
    assert response.json == {"status": "success", "message": "Fakenodo deposition created"}


def test_deposition_files_fakenodo(test_client):
    response = test_client.post('/fakenodo/api/1/files')
    assert response.status_code == 201
    assert response.json == {"status": "success", "message": "CSuccesfully created deposition 1"}


def test_delete_deposition_fakenodo(test_client):
    response = test_client.delete('/fakenodo/api/1')
    assert response.status_code == 200
    assert response.json == {"status": "success", "message": "Succesfully deleted deposition 1"}


def test_publish_deposition_fakenodo(test_client):
    response = test_client.post('/fakenodo/api/1/actions/publish')
    assert response.status_code == 202
    assert response.json == {"status": "success", "message": "Published deposition with ID 1 (Fakenodo API)"}


def test_get_deposition_fakenodo(test_client):
    response = test_client.get('/fakenodo/api/1')
    assert response.status_code == 200
    assert response.json == {
        "status": "success",
        "message": "Got deposition with ID 1 (Fakenodo API)",
        "doi": "10.5072/fakenodo.123456"
    }