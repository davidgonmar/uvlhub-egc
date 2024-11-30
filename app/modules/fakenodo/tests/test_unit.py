import pytest
from flask import Flask
from app.modules.fakenodo.routes import fakenodo_bp
from unittest.mock import patch
from app.modules.fakenodo.services import FakenodoService

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

@patch.object(FakenodoService, 'test_full_connection')
def test_test_full_connection_route(mock_test_full_connection, test_client):
    """
    Test the /fakenodo/api/test route which calls the test_full_connection method in FakenodoService.
    """
    # Mock the response from the test_full_connection method to simulate a successful test
    mock_test_full_connection.return_value = {
        "success": True,
        "message": "Successfully completed the full test on Fakenodo."
    }

    # Send GET request to the full connection route
    response = test_client.get('/fakenodo/api/test')

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Assert that the response JSON matches the expected success message
    assert response.json["success"] is True
    assert response.json["message"] == "Successfully completed the full test on Fakenodo."

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

def test_get_doi_fakenodo(test_client):
    """
    Test the GET /fakenodo/api/<depositionId>/doi route to ensure it returns the correct DOI.
    """
    deposition_id = 123  # Example deposition ID

    # Send GET request to the DOI endpoint
    response = test_client.get(f'/fakenodo/api/{deposition_id}/doi')

    # Check if the response status code is 200
    assert response.status_code == 200

    # Check if the response JSON contains the expected DOI
    expected_doi = f"10.5072/fakenodo.{deposition_id}"
    assert response.json["status"] == "success"
    assert response.json["doi"] == expected_doi
