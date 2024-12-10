import pytest
from unittest.mock import patch, MagicMock
from app.modules.explore.services import ExploreService


@pytest.fixture(scope="module")
def test_client(test_client):
    """
    Extiende la fixture de test_client para añadir elementos específicos en la base de datos
    que se usarán en los tests.
    """
    with test_client.application.app_context():
        # Aquí puedes añadir nuevos elementos a la base de datos que desees
        # para el contexto de pruebas. Asegúrate de usar db.session.add() y db.session.commit()
        pass
    yield test_client


@pytest.fixture
def explore_service():
    return ExploreService()


def test_filter_with_default_arguments(explore_service):
    with patch.object(explore_service.repository, 'filter') as mock_filter:
        # Mock de los datasets que el repositorio devolverá
        mock_datasets = [MagicMock(id=1), MagicMock(id=2)]
        mock_filter.return_value = mock_datasets
        # Llamada al método filter sin parámetros adicionales
        result = explore_service.filter()
        # Verificación del resultado
        assert result == mock_datasets
        assert len(result) == 2
        mock_filter.assert_called_once_with(
            "",
            "newest",
            "any",
            [],
            "",
            "",
            "",
            "",
            None,
            None,
            "bytes"
        )


def test_filter_with_custom_query(explore_service):
    with patch.object(explore_service.repository, 'filter') as mock_filter:
        # Mock de datasets con un query específico
        mock_datasets = [MagicMock(id=1), MagicMock(id=2)]
        mock_filter.return_value = mock_datasets
        # Parámetros personalizados para la prueba
        query = "Test Query"
        sorting = "oldest"
        tags = ["tag1", "tag2"]
        result = explore_service.filter(query=query, sorting=sorting, tags=tags)
        # Verificación del resultado
        assert result == mock_datasets
        assert len(result) == 2
        mock_filter.assert_called_once_with(
            "Test Query",
            "oldest",
            "any",
            ["tag1", "tag2"],
            "",
            "",
            "",
            "",
            None,
            None,
            "bytes"
        )


def test_filter_with_date_range(explore_service):
    with patch.object(explore_service.repository, 'filter') as mock_filter:
        # Mock de datasets filtrados por fecha
        mock_datasets = [MagicMock(id=1), MagicMock(id=2)]
        mock_filter.return_value = mock_datasets
        # Parámetros personalizados para el filtro de fecha
        start_date = "2024-01-01"
        end_date = "2024-12-31"
        result = explore_service.filter(start_date=start_date, end_date=end_date)
        # Verificación del resultado
        assert result == mock_datasets
        assert len(result) == 2
        mock_filter.assert_called_once_with(
            "",
            "newest",
            "any",
            [],
            "2024-01-01",
            "2024-12-31",
            "",
            "",
            None,
            None,
            "bytes"
        )


def test_filter_with_uvl_range(explore_service):
    with patch.object(explore_service.repository, 'filter') as mock_filter:
        # Mock de datasets filtrados por UVL
        mock_datasets = [MagicMock(id=1), MagicMock(id=2)]
        mock_filter.return_value = mock_datasets
        # Parámetros personalizados para el filtro UVL
        min_uvl = "10"
        max_uvl = "100"
        result = explore_service.filter(min_uvl=min_uvl, max_uvl=max_uvl)
        # Verificación del resultado
        assert result == mock_datasets
        assert len(result) == 2
        mock_filter.assert_called_once_with(
            "",
            "newest",
            "any",
            [],
            "",
            "",
            "10",
            "100",
            None,
            None,
            "bytes"
        )


def test_filter_with_size_range(explore_service):
    with patch.object(explore_service.repository, 'filter') as mock_filter:
        # Mock de datasets filtrados por tamaño
        mock_datasets = [MagicMock(id=1), MagicMock(id=2)]
        mock_filter.return_value = mock_datasets
        # Parámetros personalizados para el filtro de tamaño
        min_size = 500
        max_size = 2000
        size_unit = "KB"
        result = explore_service.filter(min_size=min_size, max_size=max_size, size_unit=size_unit)
        # Verificación del resultado
        assert result == mock_datasets
        assert len(result) == 2
        mock_filter.assert_called_once_with(
            "",
            "newest",
            "any",
            [],
            "",
            "",
            "",
            "",
            500,
            2000,
            "KB"
        )


def test_filter_with_multiple_parameters(explore_service):
    with patch.object(explore_service.repository, 'filter') as mock_filter:
        # Mock de datasets con múltiples filtros combinados
        mock_datasets = [MagicMock(id=1), MagicMock(id=2), MagicMock(id=3)]
        mock_filter.return_value = mock_datasets
        # Parámetros personalizados
        query = "complex search"
        tags = ["science", "data"]
        start_date = "2023-01-01"
        end_date = "2023-12-31"
        min_size = 100
        max_size = 1000
        result = explore_service.filter(
            query=query,
            tags=tags,
            start_date=start_date,
            end_date=end_date,
            min_size=min_size,
            max_size=max_size,
        )
        # Verificación del resultado
        assert result == mock_datasets
        assert len(result) == 3
        mock_filter.assert_called_once_with(
            "complex search",
            "newest",
            "any",
            ["science", "data"],
            "2023-01-01",
            "2023-12-31",
            "",
            "",
            100,
            1000,
            "bytes"
        )


def test_filter_with_specific_publication_type(explore_service):
    with patch.object(explore_service.repository, 'filter') as mock_filter:
        # Mock de datasets filtrados por tipo de publicación
        mock_datasets = [MagicMock(id=1)]
        mock_filter.return_value = mock_datasets
        # Parámetros personalizados
        publication_type = "research_paper"
        result = explore_service.filter(publication_type=publication_type)
        # Verificación del resultado
        assert result == mock_datasets
        assert len(result) == 1
        mock_filter.assert_called_once_with(
            "",
            "newest",
            "research_paper",
            [],
            "",
            "",
            "",
            "",
            None,
            None,
            "bytes"
        )


def test_filter_with_no_results(explore_service):
    with patch.object(explore_service.repository, 'filter') as mock_filter:
        # Mock de una respuesta vacía
        mock_filter.return_value = []
        # Parámetros que no coinciden con ningún dataset
        query = "nonexistent"
        tags = ["nonexistent_tag"]
        result = explore_service.filter(query=query, tags=tags)
        # Verificación del resultado
        assert result == []
        assert len(result) == 0
        mock_filter.assert_called_once_with(
            "nonexistent",
            "newest",
            "any",
            ["nonexistent_tag"],
            "",
            "",
            "",
            "",
            None,
            None,
            "bytes"
        )


def test_filter_with_invalid_date_range(explore_service):
    with patch.object(explore_service.repository, 'filter') as mock_filter:
        # Mock de una respuesta vacía o de error
        mock_filter.return_value = []
        # Parámetros con un rango de fechas inválido (fecha inicial mayor que la final)
        start_date = "2024-12-31"
        end_date = "2024-01-01"
        result = explore_service.filter(start_date=start_date, end_date=end_date)
        # Verificación del resultado
        assert result == []
        mock_filter.assert_called_once_with(
            "",
            "newest",
            "any",
            [],
            "2024-12-31",
            "2024-01-01",
            "",
            "",
            None,
            None,
            "bytes"
        )


def test_filter_with_invalid_size_range(explore_service):
    with patch.object(explore_service.repository, 'filter') as mock_filter:
        # Mock de una respuesta vacía
        mock_filter.return_value = []
        # Parámetros con un rango de tamaño inválido (mínimo mayor que el máximo)
        min_size = 2000
        max_size = 500
        result = explore_service.filter(min_size=min_size, max_size=max_size)
        # Verificación del resultado
        assert result == []
        mock_filter.assert_called_once_with(
            "",
            "newest",
            "any",
            [],
            "",
            "",
            "",
            "",
            2000,
            500,
            "bytes"
        )


def test_filter_with_invalid_uvl_range(explore_service):
    with patch.object(explore_service.repository, 'filter') as mock_filter:
        # Mock de una respuesta vacía
        mock_filter.return_value = []
        # Parámetros con un rango de UVL inválido (mínimo mayor que el máximo)
        min_uvl = "100"
        max_uvl = "10"
        result = explore_service.filter(min_uvl=min_uvl, max_uvl=max_uvl)
        # Verificación del resultado
        assert result == []
        mock_filter.assert_called_once_with(
            "",
            "newest",
            "any",
            [],
            "",
            "",
            "100",
            "10",
            None,
            None,
            "bytes"
        )


def test_filter_with_invalid_query_and_tags(explore_service):
    with patch.object(explore_service.repository, 'filter') as mock_filter:
        # Mock de una respuesta vacía
        mock_filter.return_value = []
        # Parámetros que no tienen sentido juntos (query inexistente y tags contradictorias)
        query = "!@#$%^&*()"  # Query no válida
        tags = ["nonexistent_tag1", "nonexistent_tag2"]
        result = explore_service.filter(query=query, tags=tags)
        # Verificación del resultado
        assert result == []
        mock_filter.assert_called_once_with(
            "!@#$%^&*()",
            "newest",
            "any",
            ["nonexistent_tag1", "nonexistent_tag2"],
            "",
            "",
            "",
            "",
            None,
            None,
            "bytes"
        )


def test_filter_with_unexpected_error(explore_service):
    with patch.object(explore_service.repository, 'filter', side_effect=Exception("Unexpected error")) as mock_filter:
        # Simulación de una excepción inesperada durante la ejecución
        try:
            result = explore_service.filter()
        except Exception as e:
            result = str(e)
        # Verificación de la excepción
        assert result == "Unexpected error"
        mock_filter.assert_called_once_with(
            "",
            "newest",
            "any",
            [],
            "",
            "",
            "",
            "",
            None,
            None,
            "bytes"
        )
