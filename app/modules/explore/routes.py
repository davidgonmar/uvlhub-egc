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
        
        # Calcular el average_rating para cada dataset (NO FUNCIONA, HAY QUE INTENTAR PASAR EL AVERAGE DE CADA UNO AL HTML O SCRIPT.JS)
        # Como referencia puedes mirar el de home page (modules/public/templates/index.html) y su route
        for dataset in datasets:
            average_rating = ds_rating_service.get_average_by_dataset(dataset.id) or 0.0
            dataset.average_rating = round(average_rating, 2)  # Añadir el average_rating al dataset

        return render_template('explore/index.html', form=form, query=query, datasets=datasets)

    if request.method == 'POST':
        criteria = request.get_json()
        datasets = ExploreService().filter(**criteria)
        return jsonify([dataset.to_dict() for dataset in datasets])
