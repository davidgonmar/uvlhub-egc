import pytest
from flask import Flask
from app.modules.fakenodo.routes import fakenodo_bp


@pytest.fixture(scope='module')
def test_client():
    # Create a new Flask app and register fakenodo blueprint
    app = Flask(__name__)
    app.register_blueprint(fakenodo_bp)
    
    # Return the test client to interact with the app
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
    # Assuming depositionId is 1
    response = test_client.post('/fakenodo/api/1/files')
    assert response.status_code == 201
    assert response.json == {
        "status": "success",
        "message": "Successfully uploaded files to deposition 1"
    }


def test_get_deposition_fakenodo(test_client):
    # Assuming depositionId is 1
    response = test_client.get('/fakenodo/api/1')
    assert response.status_code == 200
    assert response.json == {
        "status": "success",
        "message": "Retrieved deposition with ID 1",
        "doi": "10.5072/fakenodo.1"
    }


def test_delete_deposition_fakenodo(test_client):
    # Assuming depositionId is 1
    response = test_client.delete('/fakenodo/api/1')
    assert response.status_code == 200
    assert response.json == {
        "status": "success",
        "message": "Successfully deleted deposition 1"
    }
