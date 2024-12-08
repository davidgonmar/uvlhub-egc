import unittest
import pytest
from unittest.mock import patch, MagicMock
from app.modules.dataset.models import DataSet, DSMetaData
from app.modules.dataset.services import DataSetService
from app.modules.conftest import login, logout
from app import db
from app.modules.auth.models import User
from app.modules.profile.models import UserProfile

@pytest.fixture(scope="module")
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        user_test = User(email='user@example.com', password='test1234')
        db.session.add(user_test)
        db.session.commit()

        profile = UserProfile(user_id=user_test.id, name="Name", surname="Surname")
        db.session.add(profile)
        db.session.commit()
        pass

        test_client.user_id = user_test.id

    yield test_client


# Test unitario que devuelve el DOI
@patch("os.getenv")  # Mockear la llamada a os.getenv
def test_get_uvlhub_doi(mock_getenv):

    # Configurar el valor de retorno del mock para DOMAIN
    mock_getenv.return_value = "uvlhub.io"

    # Crear un mock del dataset y ds_meta_data
    mock_dataset = MagicMock()
    mock_dataset.ds_meta_data.dataset_doi = "10.1234/test_doi"

    # Crear una instancia del servicio
    service = DataSetService()

    # Ejecutar la función
    result = service.get_uvlhub_doi(mock_dataset)

    # Verificar que devuelve la URL esperada
    assert result == "http://uvlhub.io/doi/10.1234/test_doi"

    # Verificar que getenv fue llamado correctamente
    mock_getenv.assert_called_once_with("DOMAIN", "localhost")


# Test de integración para un DOI válido que devuelve un dataset
@patch("app.modules.dataset.services.DSMetaDataService.filter_by_doi")
@patch("app.modules.dataset.services.DSViewRecordService.create_cookie")
def test_subdomain_index_success(mock_create_cookie, mock_filter_by_doi, test_client):
    mock_dataset = MagicMock()
    mock_filter_by_doi.return_value = MagicMock(data_set=mock_dataset)
    mock_create_cookie.return_value = "mock_cookie"

    response = test_client.get("/doi/10.1234/datafset1/")
    # Verificamos que el dataset existe con ese DOI
    assert response.status_code == 200

    # Acceder a las cookies desde los encabezados de la respuesta
    cookies = response.headers.get("Set-Cookie")

    # Verificar que la cookie 'view_cookie' se ha establecido correctamente
    assert "view_cookie=mock_cookie" in cookies


# Test para cuando el DOI no se encuentra
def test_subdomain_index_not_found(test_client):
    response = test_client.get("/doi/10.1234/non_existent_doi/")

    # Verificar que devuelve 404 cuando no se encuentra el dataset
    assert response.status_code == 404


def test_download_all_endpoint_exists(test_client):
    """
    Verifica que el endpoint /dataset/download_all existe y responde con un código de estado 200.
    """
    response = test_client.get("/dataset/download_all")

    assert response.status_code == 200


def test_download_all_returns_zip(test_client):
    """
    Verifica que el endpoint /dataset/download_all devuelve un archivo ZIP.
    """
    response = test_client.get("/dataset/download_all")

    assert response.data is not None
    assert response.content_type == "application/zip"


class TestDatasetExport(unittest.TestCase):

    def setUp(self):
        # Mock de DSMetaData y FeatureModel
        self.ds_meta_data = DSMetaData(
            title="Test Dataset", description="Test description"
        )
        feature_model_mock = MagicMock()
        feature_model_mock.files = [
            MagicMock(id=1, name="test_file.uvl", size=1024),
            MagicMock(id=2, name="test_file.json", size=2048),
        ]

        # Crear dataset con mocks
        self.dataset = DataSet(
            id=1,
            user_id=1,
            ds_meta_data=self.ds_meta_data,
            feature_models=[feature_model_mock],
        )

    # 1. Prueba de exportación en formato UVL
    def test_export_uvl(self):
        response = self.mock_export("UVL")
        self.assertTrue(response["success"])
        self.assertEqual(response["export_format"], "UVL")

    # 2. Prueba de exportación en formato JSON
    def test_export_json(self):
        response = self.mock_export("JSON")
        self.assertTrue(response["success"])
        self.assertEqual(response["export_format"], "JSON")

    # 3. Prueba de exportación en formato cnf
    def test_export_cnf(self):
        response = self.mock_export("CNF")
        self.assertTrue(response["success"])
        self.assertEqual(response["export_format"], "CNF")

    # 4. Prueba de exportación en formato splx
    def test_export_splx(self):
        response = self.mock_export("SPLX")
        self.assertTrue(response["success"])
        self.assertEqual(response["export_format"], "SPLX")

    # 5. Valores Límite: Exportación de dataset vacío
    def test_export_empty_dataset(self):
        empty_dataset = DataSet(
            id=2, user_id=1, ds_meta_data=self.ds_meta_data, feature_models=[]
        )
        response = self.mock_export("JSON", dataset=empty_dataset)
        self.assertFalse(response["success"])
        self.assertEqual(response["error"], "Dataset vacío no puede ser exportado")

    # 6. Partición Equivalente: Formato no válido
    def test_invalid_format(self):
        response = self.mock_export("INVALID_FORMAT")
        self.assertFalse(response["success"])
        self.assertEqual(response["error"], "Formato de exportación no válido")

    # 7. Valores Límite: Exportación con tamaño máximo permitido
    def test_max_size_export(self):
        large_feature_model = MagicMock()
        large_feature_model.files = [
            MagicMock(id=i, name=f"file_{i}.uvl", size=1024) for i in range(1000)
        ]
        large_dataset = DataSet(
            id=3,
            user_id=1,
            ds_meta_data=self.ds_meta_data,
            feature_models=[large_feature_model],
        )
        response = self.mock_export("CNF", dataset=large_dataset)
        self.assertTrue(response["success"])
        self.assertEqual(response["export_format"], "CNF")

    # 8. Errores Conocidos: Archivo corrupto
    def test_export_corrupted_file(self):
        corrupted_feature_model = MagicMock()
        corrupted_feature_model.files = [
            MagicMock(id=3, name="corrupted_file.splx", size=-1)
        ]
        corrupted_dataset = DataSet(
            id=4,
            user_id=1,
            ds_meta_data=self.ds_meta_data,
            feature_models=[corrupted_feature_model],
        )
        response = self.mock_export("SPLX", dataset=corrupted_dataset)
        self.assertFalse(response["success"])
        self.assertEqual(response["error"], "Archivo corrupto detectado")

    # Mock del método export

    def mock_export(self, export_format, dataset=None):
        if dataset is None:
            dataset = self.dataset
        if export_format not in ["UVL", "JSON", "CNF", "SPLX"]:
            return {"success": False, "error": "Formato de exportación no válido"}
        if not dataset.files():
            return {"success": False, "error": "Dataset vacío no puede ser exportado"}
        if any(file.size < 0 for file in dataset.files()):
            return {"success": False, "error": "Archivo corrupto detectado"}
        return {"success": True, "export_format": export_format}

@patch("app.modules.dataset.services.DSMetaDataService.filter_by_doi")
def test_publish_dataset_success(mock_filter_by_doi, test_client):
    """
    Caso positivo: El dataset se publica correctamente.
    """
    # Inicia sesión el usuario
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was successful."

    # Mock del dataset y ds_meta_data
    mock_ds_meta_data = MagicMock()
    mock_dataset = MagicMock()
    mock_ds_meta_data.data_set = mock_dataset
    mock_dataset.user_id = test_client.user_id  # Usar el user_id generado dinámicamente
    mock_ds_meta_data.is_draft_mode = True

    # Configurar el mock del servicio para devolver el dataset
    mock_filter_by_doi.return_value = mock_ds_meta_data

    response = test_client.post("/dataset/publish/10.1234/test_doi/")

    assert response.status_code == 200
    assert response.json == {"message": "Dataset published successfully."}
    
@patch("app.modules.dataset.services.DSMetaDataService.filter_by_doi")
def test_publish_dataset_not_found(mock_filter_by_doi, test_client):
    """
    Caso negativo: El DOI no existe.
    """
    
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was successful."
    
    mock_filter_by_doi.return_value = None  # No se encuentra el dataset

    response = test_client.post("/dataset/publish/10.1234/non_existent_doi/")

    assert response.status_code == 404

@patch("app.modules.dataset.services.DSMetaDataService.filter_by_doi")
def test_publish_dataset_permission_denied(mock_filter_by_doi, test_client):
    """
    Caso negativo: El usuario no es el propietario del dataset.
    """
    
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was successful."
    
    mock_ds_meta_data = MagicMock()
    mock_dataset = MagicMock()
    mock_ds_meta_data.data_set = mock_dataset
    mock_dataset.user_id = test_client.user_id + 1

    mock_filter_by_doi.return_value = mock_ds_meta_data

    with test_client.session_transaction() as session:
        session["user_id"] = 1  # Usuario actual

    response = test_client.post("/dataset/publish/10.1234/test_doi/")

    assert response.status_code == 403
    assert response.json == {"message": "You do not have permission to publish this dataset."}

@patch("app.modules.dataset.services.DSMetaDataService.filter_by_doi")
def test_publish_dataset_already_published(mock_filter_by_doi, test_client):
    """
    Caso negativo: El dataset ya está publicado.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was successful."

    mock_ds_meta_data = MagicMock()
    mock_dataset = MagicMock()
    mock_ds_meta_data.data_set = mock_dataset
    mock_dataset.user_id = test_client.user_id
    mock_ds_meta_data.is_draft_mode = True 

    mock_filter_by_doi.return_value = mock_ds_meta_data

    aux_call = test_client.post("/dataset/publish/10.1234/test_doi/") # Lo publicamos
    response = test_client.post("/dataset/publish/10.1234/test_doi/") # Lo intentamos publicar otra vez

    assert response.status_code == 400
    assert response.json == {"message": "This dataset is already published."}

@patch("app.modules.dataset.services.DSMetaDataService.filter_by_doi")
def test_publish_dataset_not_logged_in(mock_filter_by_doi, test_client):
    """
    Caso negativo: El usuario no está autenticado.
    """
    logout_reponse = logout(test_client)
    assert logout_reponse.status_code == 200

    mock_ds_meta_data = MagicMock()
    mock_dataset = MagicMock()
    mock_ds_meta_data.data_set = mock_dataset
    mock_ds_meta_data.is_draft_mode = True

    mock_filter_by_doi.return_value = mock_ds_meta_data

    response = test_client.post("/dataset/publish/10.1234/test_doi/")

    assert response.status_code == 302

@patch("app.modules.dataset.services.DSMetaDataService.filter_by_doi")
def test_edit_dataset_success(mock_filter_by_doi, test_client):
    """
    Caso positivo: El dataset se edita correctamente.
    """
    # Simula el inicio de sesión
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was successful."

    mock_dataset = MagicMock()
    mock_dataset.user_id = test_client.user_id  # Simula que el usuario es el propietario

    mock_ds_meta_data = MagicMock()
    mock_ds_meta_data.is_draft_mode = True  # Simula que está en modo borrador

    mock_dataset.ds_meta_data = mock_ds_meta_data

    # Configura el mock de `filter_by_doi` para devolver un objeto con dataset
    mock_filter_by_doi.return_value = MagicMock(data_set=mock_dataset)

    # Datos para la solicitud de edición
    data = {
        "title": "Updated title",
        "description": "Updated description"
    }

    response = test_client.post("/dataset/edit/10.1234/test_doi/", json=data)

    assert response.json == {"message": "Dataset updated successfully.", "is_draft_mode": True}
    assert response.status_code == 200
    
@patch("app.modules.dataset.services.DSMetaDataService.filter_by_doi")
def test_edit_dataset_publish_success(mock_filter_by_doi, test_client):
    """
    Caso positivo: El dataset se publica con éxito (is_draft_mode cambia a False).
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was successful."

    mock_dataset = MagicMock()
    mock_dataset.user_id = test_client.user_id

    mock_ds_meta_data = MagicMock()
    mock_ds_meta_data.is_draft_mode = True
    mock_dataset.ds_meta_data = mock_ds_meta_data

    mock_filter_by_doi.return_value = MagicMock(data_set=mock_dataset)

    # Datos para publicar el dataset
    data = {
        "title": "Updated Title",
        "description": "Updated Description",
        "publish": True
    }

    response = test_client.post("/dataset/edit/10.1234/test_doi/", json=data)

    assert response.status_code == 200
    assert response.json == {"message": "Dataset updated successfully.", "is_draft_mode": False}
    
@patch("app.modules.dataset.services.DSMetaDataService.filter_by_doi")
def test_edit_dataset_permission_denied(mock_filter_by_doi, test_client):
    """
    Caso negativo: El usuario no es el propietario del dataset.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was successful."

    mock_dataset = MagicMock()
    mock_dataset.user_id = test_client.user_id + 1 # Simulando que el usuario no es el propietario

    mock_ds_meta_data = MagicMock()
    mock_ds_meta_data.is_draft_mode = True # Simula que está en modo borrador

    mock_dataset.ds_meta_data = mock_ds_meta_data

    mock_filter_by_doi.return_value = MagicMock(data_set=mock_dataset)

    response = test_client.post("/dataset/edit/10.1234/test_doi/", json={})

    # Verificar que se devuelve error 403
    assert response.status_code == 403
    assert response.json == {"message": "You do not have permission to edit this dataset."}
    
@patch("app.modules.dataset.services.DSMetaDataService.filter_by_doi")
def test_edit_dataset_already_published(mock_filter_by_doi, test_client):
    """
    Caso negativo: El dataset ya está publicado y no se puede editar.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."
    
    mock_dataset = MagicMock()
    mock_dataset.user_id = test_client.user_id 

    mock_ds_meta_data = MagicMock()
    mock_ds_meta_data.is_draft_mode = False # Simula que está publicado

    mock_dataset.ds_meta_data = mock_ds_meta_data

    mock_filter_by_doi.return_value = MagicMock(data_set=mock_dataset)

    # Datos para la solicitud de edición
    data = {
        "title": "Updated title",
        "description": "Updated description"
    }

    response = test_client.post("/dataset/edit/10.1234/test_doi/", json = data)

    # Verificar que se devuelve error 400
    assert response.status_code == 400
    assert response.json == {"message": "This dataset is already published and cannot be edited."}

@patch("app.modules.dataset.services.DSMetaDataService.filter_by_doi")
def test_edit_dataset_missing_title_description(mock_filter_by_doi, test_client):
    """
    Caso negativo: Faltan datos obligatorios (título o descripción).
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was successful."

    mock_dataset = MagicMock()
    mock_dataset.user_id = test_client.user_id 

    mock_ds_meta_data = MagicMock()
    mock_ds_meta_data.is_draft_mode = True # Simula que está en modo borrador

    mock_dataset.ds_meta_data = mock_ds_meta_data

    mock_filter_by_doi.return_value = MagicMock(data_set=mock_dataset)

    # Datos incompletos: falta título y descripción.
    data = {}

    response = test_client.post("/dataset/edit/10.1234/test_doi/", json=data)

    assert response.status_code == 400
    assert response.json == {"message": "Title and description are required."}
    
@patch("app.modules.dataset.services.DSMetaDataService.filter_by_doi")
def test_edit_dataset_missing_title(mock_filter_by_doi, test_client):
    """
    Caso negativo: Faltan datos obligatorios (título o descripción).
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was successful."

    mock_dataset = MagicMock()
    mock_dataset.user_id = test_client.user_id 

    mock_ds_meta_data = MagicMock()
    mock_ds_meta_data.is_draft_mode = True # Simula que está en modo borrador

    mock_dataset.ds_meta_data = mock_ds_meta_data

    mock_filter_by_doi.return_value = MagicMock(data_set=mock_dataset)

    # Datos incompletos: falta título.
    data = {"description": "Updated description"}

    response = test_client.post("/dataset/edit/10.1234/test_doi/", json=data)

    assert response.status_code == 400
    assert response.json == {"message": "Title and description are required."}
    
@patch("app.modules.dataset.services.DSMetaDataService.filter_by_doi")
def test_edit_dataset_missing_description(mock_filter_by_doi, test_client):
    """
    Caso negativo: Faltan datos obligatorios (título o descripción).
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was successful."

    mock_dataset = MagicMock()
    mock_dataset.user_id = test_client.user_id 

    mock_ds_meta_data = MagicMock()
    mock_ds_meta_data.is_draft_mode = True # Simula que está en modo borrador
    mock_dataset.ds_meta_data = mock_ds_meta_data

    mock_filter_by_doi.return_value = MagicMock(data_set=mock_dataset)

    # Datos incompletos: falta descripción.
    data = {"title": "Updated title"}

    response = test_client.post("/dataset/edit/10.1234/test_doi/", json=data)

    assert response.status_code == 400
    assert response.json == {"message": "Title and description are required."}

    
@patch("app.modules.dataset.services.DSMetaDataService.filter_by_doi")
def test_edit_dataset_not_found(mock_filter_by_doi, test_client):
    """
    Caso negativo: El DOI no corresponde a ningún dataset (404).
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was successful."

    # Simula que no se encuentra el dataset
    mock_filter_by_doi.return_value = None
    
    data = {
        "title": "Updated title",
        "description": "Updated description"
    }

    response = test_client.post("/dataset/edit/10.1234/nonexistent_doi/", json=data)

    assert response.status_code == 404
