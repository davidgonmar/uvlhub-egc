from flask import jsonify, make_response, request
from app.modules.dataset.models import DataSet
from app.modules.fakenodo import fakenodo_bp
from app.modules.fakenodo.services import FakenodoService
from app.modules.featuremodel.models import FeatureModel
from flask_login import login_required, current_user

base_url = "/fakenodo/api"

# Test connection (GET)
@fakenodo_bp.route(base_url + "/test_connection", methods=["GET"])
@login_required
def test_connection_fakenodo():
    service = FakenodoService()
    if service.test_connection():
        response = {"status": "success", "message": "Connected to FakenodoAPI"}
    else:
        response = {"status": "error", "message": "Connection failed"}
    return jsonify(response)


# Create a new deposition (POST)
@fakenodo_bp.route(base_url + "/depositions", methods=["POST"])
@login_required
def create_deposition():
    try:
        dataset_id = request.json.get("dataset_id")
        dataset = DataSet.query.get(dataset_id)
        
        if not dataset:
            return jsonify({"status": "error", "message": "Dataset not found."}), 404

        service = FakenodoService()
        deposition_data = service.create_new_deposition(dataset)

        return jsonify({
            "status": "success",
            "message": "Deposition created successfully.",
            "deposition": deposition_data
        }), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# Upload file to a deposition (POST)
@fakenodo_bp.route(base_url + "/<deposition_id>/files", methods=["POST"])
@login_required
def upload_file(deposition_id):
    try:
        # Get the dataset_id and feature_model_id from the form data
        dataset_id = request.form.get("dataset_id")
        feature_model_id = request.form.get("feature_model_id")

        # Fetch the Dataset and FeatureModel objects from the database
        dataset = DataSet.query.get(dataset_id)
        feature_model = FeatureModel.query.get(feature_model_id)

        # Check if dataset or feature model is not found
        if not dataset or not feature_model:
            return jsonify({"status": "error", "message": "Dataset or FeatureModel not found."}), 404

        # Create an instance of the FakenodoService
        service = FakenodoService()

        # Call the upload_file method from the service to simulate file upload
        response = service.upload_file(dataset, deposition_id, feature_model)

        # Return a success response with the file metadata
        return jsonify({
            "status": "success",
            "message": response["message"],
            "file_metadata": response.get("file_metadata", {})
        }), 201  # HTTP Status Code 201 for successful resource creation

    except Exception as e:
        # In case of an error, return a generic error message with exception details
        return jsonify({"status": "error", "message": str(e)}), 500


# Publish a deposition (PUT)
@fakenodo_bp.route(base_url + "/<deposition_id>/publish", methods=["PUT"])
@login_required
def publish_deposition(deposition_id):
    try:
        service = FakenodoService()
        message = service.publish_deposition(deposition_id)

        return jsonify({
            "status": "success",
            "message": message["message"]
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# Get a deposition's details (GET)
@fakenodo_bp.route(base_url + "/<deposition_id>", methods=["GET"])
@login_required
def get_deposition(deposition_id):
    try:
        service = FakenodoService()
        deposition = service.get_deposition(deposition_id)

        return jsonify({
            "status": "success",
            "deposition": deposition
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# Get the DOI of a deposition (GET)
@fakenodo_bp.route(base_url + "/<deposition_id>/doi", methods=["GET"])
@login_required
def get_doi(deposition_id):
    try:
        service = FakenodoService()
        doi = service.get_doi(deposition_id)

        return jsonify({
            "status": "success",
            "doi": doi
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# Get all depositions (GET)
@fakenodo_bp.route(base_url + "/depositions", methods=["GET"])
@login_required
def get_all_depositions():
    try:
        service = FakenodoService()
        depositions = service.get_all_depositions()

        return jsonify({
            "status": "success",
            "depositions": depositions
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# Delete a deposition (DELETE)
@fakenodo_bp.route(base_url + "/<deposition_id>", methods=["DELETE"])
@login_required
def delete_deposition(deposition_id):
    try:
        service = FakenodoService()
        message = service.delete_deposition(deposition_id)

        return jsonify({
            "status": "success",
            "message": message["message"]
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
