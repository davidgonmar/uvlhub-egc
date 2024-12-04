import logging

from flask import render_template

from app.modules.featuremodel.services import FeatureModelService
from app.modules.public import public_bp
from app.modules.dataset.services import DSRatingService, DataSetService

ds_rating_service = DSRatingService()

logger = logging.getLogger(__name__)


@public_bp.route("/")
def index():
    logger.info("Access index")
    dataset_service = DataSetService()
    feature_model_service = FeatureModelService()

    # Statistics: total datasets and feature models
    datasets_counter = dataset_service.count_synchronized_datasets()
    feature_models_counter = feature_model_service.count_feature_models()

    # Statistics: total downloads
    total_dataset_downloads = dataset_service.total_dataset_downloads()
    total_feature_model_downloads = feature_model_service.total_feature_model_downloads()

    # Statistics: total views
    total_dataset_views = dataset_service.total_dataset_views()
    total_feature_model_views = feature_model_service.total_feature_model_views()

    # Obtener la lista de datasets y calcular el average_rating para cada uno
    datasets = dataset_service.latest_synchronized()
    for dataset in datasets:
        dataset.average_rating = round(ds_rating_service.get_average_by_dataset(dataset.id) or 0.0, 2)

    return render_template(
        "public/index.html",
        datasets=datasets,
        datasets_counter=datasets_counter,
        feature_models_counter=feature_models_counter,
        total_dataset_downloads=total_dataset_downloads,
        total_feature_model_downloads=total_feature_model_downloads,
        total_dataset_views=total_dataset_views,
        total_feature_model_views=total_feature_model_views
    )
