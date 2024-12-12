import pytest
from unittest.mock import MagicMock, patch
from app.modules.featuremodel.services import FMRatingService
import unittest
import pytest
from unittest.mock import patch, MagicMock
from app.modules.dataset.models import DataSet, DSMetaData, DSRating
from app.modules.dataset.services import DataSetService, DSRatingService
from app.modules.dataset.repositories import DataSetRepository
from app.modules.conftest import login, logout
from app import db
from app.modules.auth.models import User
from app.modules.profile.models import UserProfile


# ===================================================== UNIT TESTS FOR MODEL RATING SERVICE =====================================================
@pytest.fixture
def fm_rating_service():
    return FMRatingService()

def test_get(fm_rating_service):
    with patch('app.modules.featuremodel.services.FMRatingRepository.get') as mock_get:
        ret = MagicMock()
        mock_get.return_value = ret
        assert fm_rating_service.get(1, 2) == ret
        mock_get.assert_called_once_with(1, 2)

def test_get_average_by_feature_model(fm_rating_service):
    with patch('app.modules.featuremodel.services.FMRatingRepository.get_average_by_feature_model') as mock_get_avg:
        ret = MagicMock()
        mock_get_avg.return_value = ret
        assert fm_rating_service.get_average_by_feature_model(1) == ret
        mock_get_avg.assert_called_once_with(1)

def test_create_or_update(fm_rating_service):
    with patch('app.modules.featuremodel.services.FMRatingRepository.create_or_update') as mock_create_or_update:
        ret = MagicMock()
        mock_create_or_update.return_value = ret
        assert fm_rating_service.create_or_update(1, 2, 3) == ret
        mock_create_or_update.assert_called_once_with(1, 2, 3)


# ===================================================== UNIT TESTS FOR MODEL RATING ENDPOINTS =====================================================
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

@patch("app.modules.featuremodel.services.FMRatingService.create_or_update")
def test_rate_model_success(mock_create_or_update, test_client):
    """
    Caso positivo: El usuario califica un modelo con éxito.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was successful."

    data = {
        "model_id": 1,
        "rating": 5
    }

    response = test_client.post("/featuremodel/rate", json=data)

    assert response.status_code == 200

    mock_create_or_update.assert_called_once_with(1, test_client.user_id, 5)
    assert response.json == {"message": "Rating saved successfully"}

@patch("app.modules.featuremodel.services.FMRatingService.create_or_update")
def test_rate_model_invalid_request_both(mock_create_or_update, test_client):
    """
    Caso negativo: La solicitud es inválida.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was successful."

    data = {
        "model_id": None,
        "rating": None
    }

    response = test_client.post("/featuremodel/rate", json=data)

    assert response.status_code == 400
    assert response.json == {"message": "Invalid request"}

    mock_create_or_update.assert_not_called()

@patch("app.modules.featuremodel.services.FMRatingService.create_or_update")
def test_rate_model_invalid_request_rating(mock_create_or_update, test_client):
    """
    Caso negativo: La solicitud es inválida.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was successful."

    data = {
        "model_id": 1,
        "rating": None
    }

    response = test_client.post("/featuremodel/rate", json=data)

    assert response.status_code == 400
    assert response.json == {"message": "Invalid request"}

    mock_create_or_update.assert_not_called()

@patch("app.modules.featuremodel.services.FMRatingService.create_or_update")
def test_rate_model_invalid_request_model(mock_create_or_update, test_client):
    """
    Caso negativo: La solicitud es inválida.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was successful."

    data = {
        "model_id": None,
        "rating": 5
    }

    response = test_client.post("/featuremodel/rate", json=data)

    assert response.status_code == 400
    assert response.json == {"message": "Invalid request"}

    mock_create_or_update.assert_not_called()

@patch("app.modules.featuremodel.services.FMRatingService.create_or_update")
def test_rate_model_permission_denied(mock_create_or_update, test_client):
    """
    Caso negativo: El usuario no está autenticado.
    """
    logout_response = logout(test_client)
    assert logout_response.status_code == 200

    data = {
        "model_id": 1,
        "rating": 5
    }

    response = test_client.post("/featuremodel/rate", json=data)

    assert response.status_code == 302
    mock_create_or_update.assert_not_called()
