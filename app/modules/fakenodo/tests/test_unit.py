import pytest
from unittest.mock import MagicMock
from app.modules.fakenodo.services import FakenodoService


@pytest.fixture
def fakenodo_service():
    # Mocking the repository inside the FakenodoService
    service = FakenodoService()
    service.deposition_repository = MagicMock()  # Mock the FakenodoRepository
    return service


@pytest.fixture
def mock_dataset():
    mock_ds = MagicMock()
    mock_ds.id = 1  # Set mock dataset ID
    mock_ds.ds_meta_data.title = "Test Dataset"
    mock_ds.ds_meta_data.description = "A test dataset."
    mock_ds.ds_meta_data.authors = []  # Mock authors list
    mock_ds.ds_meta_data.tags = "tag1, tag2"
    mock_ds.ds_meta_data.publication_type.value = "none"  # Mock publication type
    return mock_ds


@pytest.fixture
def mock_feature_model():
    # Create a mock feature model
    mock_fm = MagicMock()
    mock_fm.fm_meta_data.uvl_filename = "test_file.uvl"
    return mock_fm


def test_test_connection(fakenodo_service):
    # Test the connection to Fakenodo
    assert fakenodo_service.test_connection() is True


def test_create_new_deposition(fakenodo_service, mock_dataset):
    # Mock the repository method
    mock_deposition = MagicMock()
    mock_deposition.id = 123
    mock_deposition.doi = "10.5281/dataset123"
    mock_deposition.metadata = {
        "title": "Test Dataset",
        "description": "A test dataset.",
        "creators": [],
        "keywords": ["tag1", "tag2", "uvlhub"],
        "license": "CC-BY-4.0"
    }
    
    fakenodo_service.deposition_repository.create_new_deposition.return_value = mock_deposition

    # Test creating a new deposition
    deposition = fakenodo_service.create_new_deposition(mock_dataset)

    # Check if deposition ID and DOI are generated
    assert "deposition_id" in deposition
    assert "doi" in deposition
    assert deposition["doi"].startswith("10.5281/dataset")

    # Check that the repository method was called with the correct arguments
    fakenodo_service.deposition_repository.create_new_deposition.assert_called_once_with(
        deposition["doi"], deposition["dep_metadata"]
    )


