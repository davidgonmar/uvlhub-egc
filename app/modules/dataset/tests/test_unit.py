import pytest
from unittest.mock import patch, MagicMock
from app.modules.dataset.models import  DataSet, DSMetaData
from app.modules.dataset.services import DataSetService
import unittest

@pytest.fixture(scope="module")
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        # Add HERE new elements to the database that you want to exist in the test context.
        # DO NOT FORGET to use db.session.add(<element>) and db.session.commit() to save the data.
        pass

    yield test_client


# Test unitario que devuelve el DOI
@patch('os.getenv')  # Mockear la llamada a os.getenv
def test_get_uvlhub_doi(mock_getenv):

    # Configurar el valor de retorno del mock para DOMAIN
    mock_getenv.return_value = 'uvlhub.io'

    # Crear un mock del dataset y ds_meta_data
    mock_dataset = MagicMock()
    mock_dataset.ds_meta_data.dataset_doi = '10.1234/test_doi'

    # Crear una instancia del servicio
    service = DataSetService()

    # Ejecutar la función
    result = service.get_uvlhub_doi(mock_dataset)

    # Verificar que devuelve la URL esperada
    assert result == 'http://uvlhub.io/doi/10.1234/test_doi'

    # Verificar que getenv fue llamado correctamente
    mock_getenv.assert_called_once_with('DOMAIN', 'localhost')


# Test de integración para un DOI válido que devuelve un dataset
@patch('app.modules.dataset.services.DSMetaDataService.filter_by_doi')
@patch('app.modules.dataset.services.DSViewRecordService.create_cookie')
def test_subdomain_index_success(mock_create_cookie, mock_filter_by_doi, test_client):
    mock_dataset = MagicMock()
    mock_filter_by_doi.return_value = MagicMock(data_set=mock_dataset)
    mock_create_cookie.return_value = 'mock_cookie'

    response = test_client.get('/doi/10.1234/datafset1/')
    # Verificamos que el dataset existe con ese DOI
    assert response.status_code == 200

    # Acceder a las cookies desde los encabezados de la respuesta
    cookies = response.headers.get('Set-Cookie')

    # Verificar que la cookie 'view_cookie' se ha establecido correctamente
    assert 'view_cookie=mock_cookie' in cookies


# Test para cuando el DOI no se encuentra
def test_subdomain_index_not_found(test_client):
    response = test_client.get('/doi/10.1234/non_existent_doi/')

    # Verificar que devuelve 404 cuando no se encuentra el dataset
    assert response.status_code == 404


def test_download_all_endpoint_exists(test_client):
    """
    Verifica que el endpoint /dataset/download_all existe y responde con un código de estado 200.
    """
    response = test_client.get('/dataset/download_all')

    assert response.status_code == 200

def test_download_all_returns_zip(test_client):
    """
    Verifica que el endpoint /dataset/download_all devuelve un archivo ZIP.
    """
    response = test_client.get('/dataset/download_all')

    assert response.data is not None
    assert response.content_type == 'application/zip'


class TestDatasetExport(unittest.TestCase):

    def setUp(self):
        # Mock de DSMetaData y FeatureModel
        self.ds_meta_data = DSMetaData(title="Test Dataset", description="Test description")
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
        self.assertEqual(response["format"], "UVL")

    # 2. Prueba de exportación en formato JSON
    def test_export_json(self):
        response = self.mock_export("JSON")
        self.assertTrue(response["success"])
        self.assertEqual(response["format"], "JSON")
    
    # 3. Prueba de exportación en formato cnf
    def test_export_cnf(self):
        response = self.mock_export("CNF")
        self.assertTrue(response["success"])
        self.assertEqual(response["format"], "CNF")
    
    # 4. Prueba de exportación en formato splx
    def test_export_splx(self):
        response = self.mock_export("SPLX")
        self.assertTrue(response["success"])
        self.assertEqual(response["format"], "SPLX")

    # 5. Valores Límite: Exportación de dataset vacío
    def test_export_empty_dataset(self):
        empty_dataset = DataSet(id=2, user_id=1, ds_meta_data=self.ds_meta_data, feature_models=[])
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
        large_feature_model.files = [MagicMock(id=i, name=f"file_{i}.uvl", size=1024) for i in range(1000)]
        large_dataset = DataSet(id=3, user_id=1, ds_meta_data=self.ds_meta_data, feature_models=[large_feature_model])
        response = self.mock_export("CNF", dataset=large_dataset)
        self.assertTrue(response["success"])
        self.assertEqual(response["format"], "CNF")

    #8. Errores Conocidos: Archivo corrupto
    def test_export_corrupted_file(self):
        corrupted_feature_model = MagicMock()
        corrupted_feature_model.files = [MagicMock(id=3, name="corrupted_file.splx", size=-1)]
        corrupted_dataset = DataSet(
            id=4, user_id=1, ds_meta_data=self.ds_meta_data, feature_models=[corrupted_feature_model]
        )
        response = self.mock_export("SPLX", dataset=corrupted_dataset)
        self.assertFalse(response["success"])
        self.assertEqual(response["error"], "Archivo corrupto detectado")

    # Mock del método export
    def mock_export(self, format, dataset=None):
        if dataset is None:
            dataset = self.dataset
        if format not in ["UVL", "JSON", "CNF", "SPLX"]:
            return {"success": False, "error": "Formato de exportación no válido"}
        if not dataset.files():
            return {"success": False, "error": "Dataset vacío no puede ser exportado"}
        if any(file.size < 0 for file in dataset.files()):
            return {"success": False, "error": "Archivo corrupto detectado"}
        return {"success": True, "format": format}
