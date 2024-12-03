from flask import render_template, request, jsonify

from app.modules.explore import explore_bp
from app.modules.explore.forms import ExploreForm
from app.modules.explore.services import ExploreService
from app.modules.dataset.services import DSRatingService

ds_rating_service = DSRatingService()

@explore_bp.route('/explore', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        query = request.args.get('query', '')
        form = ExploreForm()
        
        # Filtrar los datasets
        datasets = ExploreService().filter(query=query)
        return render_template('explore/index.html', form=form, query=query, datasets=datasets)

    if request.method == 'POST':
        criteria = request.get_json()
        datasets = ExploreService().filter(**criteria)
        return jsonify([dataset.to_dict() for dataset in datasets])
