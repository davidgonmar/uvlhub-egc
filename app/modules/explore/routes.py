from flask import render_template, request, jsonify, session

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

        # Obtener los datasets de ExploreService
        datasets = ExploreService().filter(query=query)

        # Filtrar aquellos datasets que no estén en modo borrador (is_draft_mode=False)
        datasets = [dataset for dataset in datasets if not dataset.ds_meta_data.is_draft_mode]

        return render_template('explore/index.html', form=form, query=query, datasets=datasets)

    if request.method == 'POST':
        criteria = request.get_json()

        # Guardar los criterios en la sesión
        session['explore_criteria'] = criteria

        # Obtener los datasets de ExploreService
        datasets = ExploreService().filter(**criteria)

        # Filtrar aquellos datasets que no estén en modo borrador (is_draft_mode=False)
        datasets = [dataset for dataset in datasets if not dataset.ds_meta_data.is_draft_mode]

        return jsonify([dataset.to_dict() for dataset in datasets])

