from app.modules.featuremodel.services import FMRatingService
from flask import (
    render_template,
    request,
    jsonify
)
from app.modules.featuremodel import featuremodel_bp
from flask_login import login_required, current_user

fm_rating_service = FMRatingService()

@featuremodel_bp.route('/featuremodel', methods=['GET'])
def index():
    return render_template('featuremodel/index.html')

@login_required
@featuremodel_bp.route("/featuremodel/rate", methods=["POST"])
def rate():
    data = request.get_json()
    model_id = data.get("model_id")
    rating = data.get("rating")
    

    if not model_id or not rating:
        return jsonify({"message": "Invalid request"}), 400

    fm_rating_service.create_or_update(model_id, current_user.id, rating)

    return jsonify({
        "message": "Rating saved successfully",
    }), 200

