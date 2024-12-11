import pytest
from unittest.mock import MagicMock, patch
from app.modules.featuremodel.services import FMRatingService

# ===================================================== UNIT TESTS FOR FMRatingService =====================================================
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