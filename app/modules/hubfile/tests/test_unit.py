import pytest
from unittest.mock import patch, MagicMock
from app import db
from app.modules.auth.models import User
from app.modules.conftest import login, logout

@pytest.fixture(scope='module')
def test_client(test_client):
    """
    Fixture que inicializa un cliente de pruebas y agrega un usuario de prueba.
    """
    with test_client.application.app_context():
        user_test = User(email='user@example.com', password='test1234')
        db.session.add(user_test)
        db.session.commit()

        test_client.user_id = user_test.id

    yield test_client

def test_sample_assertion(test_client):
    """
    Sample test to verify that the test framework and environment are working correctly.
    It does not communicate with the Flask application; it only performs a simple assertion to
    confirm that the tests in this module can be executed.
    """
    greeting = "Hello, World!"
    assert greeting == "Hello, World!", "The greeting does not coincide with 'Hello, World!'"
    
@patch("app.modules.hubfile.services.HubfileService.get_or_404")
@patch("os.path.exists")
@patch("os.remove")
def test_delete_file_success(mock_os_remove, mock_os_path_exists, mock_get_or_404, test_client):
    """
    Caso positivo: El archivo se elimina correctamente.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200

    mock_file = MagicMock()
    mock_file.id = 123
    mock_file.feature_model.data_set.user_id = test_client.user_id
    mock_file.name = "test_file.txt"
    mock_get_or_404.return_value = mock_file
    mock_os_path_exists.return_value = True

    response = test_client.post("/file/delete", json={"file_id": mock_file.id})

    assert response.status_code == 200
    assert response.json == {"success": True, "message": "File deleted successfully"}
    mock_os_remove.assert_called_once()

@patch("app.modules.hubfile.services.HubfileService.get_or_404")
def test_delete_file_permission_denied(mock_get_or_404, test_client):
    """
    Caso negativo: El usuario no tiene permiso para eliminar el archivo.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200

    mock_file = MagicMock()
    mock_file.id = 123
    mock_file.feature_model.data_set.user_id = test_client.user_id + 1
    mock_get_or_404.return_value = mock_file

    response = test_client.post("/file/delete", json={"file_id": mock_file.id})

    assert response.status_code == 403
    assert response.json == {"success": False, "error": "You do not have permission to delete this file"}

@patch("app.modules.hubfile.services.HubfileService.get_or_404")
@patch("os.path.exists")
def test_delete_file_not_found(mock_os_path_exists, mock_get_or_404, test_client):
    """
    Caso negativo: El archivo no existe en el sistema.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200

    mock_file = MagicMock()
    mock_file.id = 123
    mock_file.feature_model.data_set.user_id = test_client.user_id
    mock_file.name = "test_file.txt"
    mock_get_or_404.return_value = mock_file
    mock_os_path_exists.return_value = False

    response = test_client.post("/file/delete", json={"file_id": mock_file.id})

    assert response.status_code == 404
    assert response.json == {"success": False, "error": "File not found"}

@patch("app.modules.hubfile.services.HubfileService.get_or_404")
@patch("os.path.exists")
@patch("os.remove")
def test_delete_file_unexpected_error(mock_os_remove, mock_os_path_exists, mock_get_or_404, test_client):
    """
    Caso negativo: Error inesperado al eliminar el archivo.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200

    mock_file = MagicMock()
    mock_file.id = 123
    mock_file.feature_model.data_set.user_id = test_client.user_id
    mock_file.name = "test_file.txt"
    mock_get_or_404.return_value = mock_file
    mock_os_path_exists.return_value = True

    mock_os_remove.side_effect = Exception("Unexpected error")

    response = test_client.post("/file/delete", json={"file_id": mock_file.id})

    assert response.status_code == 500
    assert response.json == {"success": False, "error": "Unexpected error"}

def test_delete_file_not_logged_in(test_client):
    """
    Caso negativo: El usuario no está autenticado.
    """
    logout_response = logout(test_client)
    assert logout_response.status_code == 200

    mock_file = MagicMock()
    mock_file.id = 123
    response = test_client.post("/file/delete", json={"file_id": mock_file.id})

    assert response.status_code == 302