from app.modules.featuremodel.repositories import FMMetaDataRepository, FeatureModelRepository
from app.modules.hubfile.services import HubfileService
from core.services.BaseService import BaseService
from typing import Optional
from app.modules.featuremodel.models import FMRating
from app.modules.featuremodel.repositories import FMRatingRepository

class FeatureModelService(BaseService):
    def __init__(self):
        super().__init__(FeatureModelRepository())
        self.hubfile_service = HubfileService()

    def total_feature_model_views(self) -> int:
        return self.hubfile_service.total_hubfile_views()

    def total_feature_model_downloads(self) -> int:
        return self.hubfile_service.total_hubfile_downloads()

    def count_feature_models(self):
        return self.repository.count_feature_models()

    class FMMetaDataService(BaseService):
        def __init__(self):
            super().__init__(FMMetaDataRepository())

class FMRatingService(BaseService):
    def __init__(self):
        super().__init__(FMRatingRepository())

    def get(self, feature_model_id: int, user_id: int) -> Optional[FMRating]:
        return self.repository.get(feature_model_id, user_id)
    
    def get_average_by_feature_model(self, feature_model_id: int) -> float:
        return self.repository.get_average_by_feature_model(feature_model_id)
    
    def create_or_update(self, feature_model_id: int, user_id: int, rating: int) -> FMRating:
        return self.repository.create_or_update(feature_model_id, user_id, rating)