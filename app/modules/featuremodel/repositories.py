
from sqlalchemy import func
from app.modules.featuremodel.models import FMMetaData, FeatureModel
from core.repositories.BaseRepository import BaseRepository
from typing import Optional
from app.modules.featuremodel.models import FMRating

class FeatureModelRepository(BaseRepository):
    def __init__(self):
        super().__init__(FeatureModel)

    def count_feature_models(self) -> int:
        max_id = self.model.query.with_entities(func.max(self.model.id)).scalar()
        return max_id if max_id is not None else 0


class FMMetaDataRepository(BaseRepository):
    def __init__(self):
        super().__init__(FMMetaData)

class FMRatingRepository(BaseRepository):
    def __init__(self):
        super().__init__(FMRating)

    def get(self, feature_model_id: int, user_id: int) -> Optional[FMRating]:
        return self.model.query.filter_by(feature_model_id=feature_model_id, user_id=user_id).first()

    def get_average_by_feature_model(self, feature_model_id: int) -> float:
        return self.model.query.filter_by(feature_model_id=feature_model_id).with_entities(func.avg(self.model.rating)).scalar()

    def create_or_update(self, feature_model_id: int, user_id: int, rating: int) -> FMRating:
        existing_rating = self.get(feature_model_id, user_id)
        if existing_rating:
            existing_rating.rating = rating
            existing_rating.save()
        else:
            existing_rating = self.create(
                user_id=user_id,
                feature_model_id=feature_model_id,
                rating=rating,
            )
        return existing_rating