from flask import jsonify, make_response
from app.modules.fakenodo import fakenodo_bp

base_url = "/fakenodo/api"

@fakenodo_bp.route(base_url, methods=["GET"])
def test_connection_fakenodo():
    response = {"status": "success", "message": "Connected to FakenodoAPI"}
    return jsonify(response)

@fakenodo_bp.route(base_url, methods=["POST"])
def create_fakenodo():
    response = {"status": "success", "message": "Fakenodo deposition created"}
    return make_response(jsonify(response), 201)

@fakenodo_bp.route(base_url + "/<depositionId>/files", methods=["POST"])
def deposition_files_fakenodo(depositionId):
    response = {
        "status": "success",
        "message": f"CSuccesfully created deposition {depositionId}",
    }
    return make_response(jsonify(response), 201)

@fakenodo_bp.route(base_url + "/<depositionId>", methods=["DELETE"])
def delete_deposition_fakenodo(depositionId):
    response = {
        "status": "success",
        "message": f"Succesfully deleted deposition {depositionId}",
    }
    return make_response(jsonify(response), 200)

@fakenodo_bp.route(base_url + "/<depositionId>/actions/publish", methods=["POST"])
def publish_deposition_fakenodo(depositionId):
    response = {
        "status": "success",
        "message": f"Published deposition with ID {depositionId} (Fakenodo API)",
    }
    return make_response(jsonify(response), 202)

@fakenodo_bp.route(base_url + "/<depositionId>", methods=["GET"])
def get_deposition_fakenodo(depositionId):
    response = {
        "status": "success",
        "message": f"Got deposition with ID {depositionId} (Fakenodo API)",
        "doi": "10.5072/fakenodo.123456",
    }
    return make_response(jsonify(response), 200)