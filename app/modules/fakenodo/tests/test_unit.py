import pytest
from unittest.mock import MagicMock
from unittest.mock import patch
from app.modules.fakenodo.services import FakenodoService
from app.modules.dataset.models import DataSet
from app.modules.featuremodel.models import FeatureModel
from flask_login import current_user
import os


@pytest.fixture
def fakenodo_service():
    return FakenodoService()


@pytest.fixture
def mock_dataset():
    # Create a mock dataset
    mock_ds = MagicMock()
    mock_ds.id = 1
    mock_ds.ds_meta_data.title = "Test Dataset"
    mock_ds.ds_meta_data.description = "A test dataset."
    mock_ds.ds_meta_data.authors = []
    mock_ds.ds_meta_data.tags = "tag1, tag2"
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
    # Test creating a new deposition
    deposition = fakenodo_service.create_new_deposition(mock_dataset)
    
    # Check if deposition ID and DOI are generated
    assert "deposition_id" in deposition
    assert "doi" in deposition
    assert deposition["doi"].startswith("10.5281/fakenodo.")


def test_upload_file(fakenodo_service, mock_dataset, mock_feature_model):
    # Test uploading a file to a deposition
    
    # Create a new deposition
    deposition = fakenodo_service.create_new_deposition(mock_dataset)
    deposition_id = deposition["deposition_id"]
    
    # Mock current_user using unittest.mock.patch, patching it at the correct import location
    with patch('app.modules.fakenodo.services.current_user') as mock_current_user:
        mock_current_user.id = 123
        
        # Simulate the file upload
        result = fakenodo_service.upload_file(mock_dataset, deposition_id, mock_feature_model)
    
    # Check if the success message is in the result
    assert "File test_file.uvl uploaded successfully." in result["message"]
    
    # Validate the returned file metadata
    assert "file_metadata" in result
    assert result["file_metadata"]["file_name"] == "test_file.uvl"
    assert result["file_metadata"]["file_url"] == "/uploads/user_123/dataset_1/test_file.uvl"
    assert "upload_time" in result["file_metadata"]
    
    # Check if the file is saved on disk
    file_path = os.path.join("uploads", "user_123", f"dataset_{mock_dataset.id}", "test_file.uvl")
    assert os.path.exists(file_path)

    # Optionally, you can check if the file content is as expected
    with open(file_path, 'r') as file:
        content = file.read()
        assert content == "Simulated file content."


def test_publish_deposition(fakenodo_service, mock_dataset):
    # Test publishing a deposition
    deposition = fakenodo_service.create_new_deposition(mock_dataset)
    deposition_id = deposition["deposition_id"]
    
    result = fakenodo_service.publish_deposition(deposition_id)
    
    # Check if deposition is published
    assert "Deposition published successfully." in result["message"]
    assert fakenodo_service.depositions[deposition_id]["published"] is True


def test_get_deposition(fakenodo_service, mock_dataset):
    # Test retrieving a deposition
    deposition = fakenodo_service.create_new_deposition(mock_dataset)
    deposition_id = deposition["deposition_id"]
    
    result = fakenodo_service.get_deposition(deposition_id)
    
    # Check if the returned deposition matches the metadata
    assert "metadata" in result
    assert result["metadata"]["title"] == mock_dataset.ds_meta_data.title


def test_get_doi(fakenodo_service, mock_dataset):
    # Test retrieving DOI of a deposition
    deposition = fakenodo_service.create_new_deposition(mock_dataset)
    deposition_id = deposition["deposition_id"]
    
    result = fakenodo_service.get_doi(deposition_id)
    
    # Check if the returned DOI matches the generated one
    assert result.startswith("10.5281/fakenodo.")


def test_get_all_depositions(fakenodo_service, mock_dataset):
    # Test getting all depositions
    fakenodo_service.create_new_deposition(mock_dataset)
    
    result = fakenodo_service.get_all_depositions()
    
    # Check if all depositions are returned
    assert len(result) == 1
    assert "metadata" in result[next(iter(result))]


def test_delete_deposition(fakenodo_service, mock_dataset):
    # Test deleting a deposition
    deposition = fakenodo_service.create_new_deposition(mock_dataset)
    deposition_id = deposition["deposition_id"]
    
    result = fakenodo_service.delete_deposition(deposition_id)
    
    # Check if the deposition is deleted
    assert "Deposition deleted successfully." in result["message"]
    assert deposition_id not in fakenodo_service.depositions
