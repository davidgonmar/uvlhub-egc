from flask import jsonify, make_response
from app.modules.fakenodo import fakenodo_bp


base_url = "/fakenodo/api"


# Test connection (GET)
@fakenodo_bp.route(base_url, methods=["GET"])
def test_connection_fakenodo():
    response = {"status": "success", "message": "Connected to FakenodoAPI"}
    return jsonify(response)


# Create deposition (POST)
@fakenodo_bp.route(base_url, methods=["POST"])
def create_fakenodo():
    response = {"status": "success", "message": "Fakenodo deposition created"}
    return make_response(jsonify(response), 201)


# Upload files to deposition (POST)
@fakenodo_bp.route(base_url + "/<depositionId>/files", methods=["POST"])
def deposition_files_fakenodo(depositionId):
    response = {
        "status": "success",
        "message": f"Successfully uploaded files to deposition {depositionId}",
    }
    return make_response(jsonify(response), 201)


# Get deposition (GET)
@fakenodo_bp.route(base_url + "/<depositionId>", methods=["GET"])
def get_deposition_fakenodo(depositionId):
    response = {
        "status": "success",
        "message": f"Retrieved deposition with ID {depositionId}",
        "doi": f"10.5072/fakenodo.{depositionId}",
    }
    return make_response(jsonify(response), 200)


# Delete deposition (DELETE)
@fakenodo_bp.route(base_url + "/<depositionId>", methods=["DELETE"])
def delete_deposition_fakenodo(depositionId):
    response = {
        "status": "success",
        "message": f"Successfully deleted deposition {depositionId}",
    }
    return make_response(jsonify(response), 200)
