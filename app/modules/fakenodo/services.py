import logging
import os
from flask import jsonify, Response
from app.modules.dataset.models import DataSet
from app.modules.featuremodel.models import FeatureModel
from core.configuration.configuration import uploads_folder_name
from dotenv import load_dotenv
from flask_login import current_user
from core.services.BaseService import BaseService
import requests

logger = logging.getLogger(__name__)

load_dotenv()

class FakenodoService(BaseService):

    def get_fakenodo_url(self):
        """
        Return the base URL for Fakenodo API (for local development or testing).
        """
        FLASK_ENV = os.getenv("FLASK_ENV", "development")
        if FLASK_ENV == "development":
            return "http://localhost/fakenodo/api"  # Fakenodo API for local environment
        else:
            # In production, you could point to the real Fakenodo API if applicable
            return "http://localhost/fakenodo/api"

    def __init__(self):
        # Call the BaseService constructor with the repository argument
        self.FAKENODO_API_URL = self.get_fakenodo_url()
        self.headers = {"Content-Type": "application/json"}
    
    def test_connection(self) -> bool:
        """
        Test connection to the Fakenodo API (GET /fakenodo/api).
        """
        response = requests.get(self.FAKENODO_API_URL)
        if response.status_code == 200:
            logger.info("Successfully connected to Fakenodo API.")
            return True
        else:
            logger.error(f"Failed to connect to Fakenodo API. Status Code: {response.status_code}")
            return False

    def test_full_connection(self) -> Response:
        """
        Test the full connection by interacting with Fakenodo API: create, upload, and delete.
        """
        # Simulate creating a deposition (POST request)
        response = requests.post(self.FAKENODO_API_URL)
        if response.status_code != 201:
            return jsonify({
                "success": False,
                "message": "Failed to create a test deposition on Fakenodo."
            })

        deposition_id = 789  # In real implementation, you'd extract this from the response
        file_upload_response = self.upload_file(deposition_id)
        if file_upload_response["status"] != "success":
            return jsonify({
                "success": False,
                "message": f"Failed to upload file for deposition {deposition_id}."
            })

        # Simulate deleting a deposition (DELETE request)
        delete_response = self.delete_deposition(deposition_id)
        if delete_response["status"] != "success":
            return jsonify({
                "success": False,
                "message": f"Failed to delete deposition {deposition_id}."
            })

        return jsonify({"success": True, "message": "Successfully completed the full test on Fakenodo."})

    def create_new_deposition(self, dataset: DataSet) -> dict:
        """
        Simulate creating a new deposition on Fakenodo (POST /fakenodo/api).
        """
        data = {
            "title": dataset.ds_meta_data.title,
            "upload_type": "dataset" if dataset.ds_meta_data.publication_type.value == "none" else "publication",
            "description": dataset.ds_meta_data.description,
            "creators": [{"name": author.name} for author in dataset.ds_meta_data.authors],
            "keywords": dataset.ds_meta_data.tags.split(", ") if dataset.ds_meta_data.tags else ["uvlhub"]
        }

        response = requests.post(self.FAKENODO_API_URL, json=data, headers=self.headers)
        if response.status_code == 201:
            return response.json()  # Mock response with deposition ID and status
        else:
            raise Exception(f"Failed to create deposition on Fakenodo. Response: {response.content}")

    def upload_file(self, deposition_id: int, feature_model: FeatureModel = None) -> dict:
        """
        Simulate uploading a file to a deposition (POST /fakenodo/api/<depositionId>/files).
        """
        # Simulate file upload logic
        response = requests.post(f"{self.FAKENODO_API_URL}/{deposition_id}/files", headers=self.headers)
        if response.status_code == 201:
            return {"status": "success", "message": f"Successfully uploaded files to deposition {deposition_id}"}
        else:
            return {"status": "failure", "message": f"Failed to upload files to deposition {deposition_id}"}

    def get_deposition(self, deposition_id: int) -> dict:
        """
        Simulate retrieving a deposition from Fakenodo (GET /fakenodo/api/<depositionId>).
        """
        response = requests.get(f"{self.FAKENODO_API_URL}/{deposition_id}", headers=self.headers)
        if response.status_code == 200:
            return response.json()  # Returns deposition details with DOI
        else:
            raise Exception(f"Failed to get deposition from Fakenodo. Response: {response.content}")

    def delete_deposition(self, deposition_id: int) -> dict:
        """
        Simulate deleting a deposition from Fakenodo (DELETE /fakenodo/api/<depositionId>).
        """
        response = requests.delete(f"{self.FAKENODO_API_URL}/{deposition_id}", headers=self.headers)
        if response.status_code == 200:
            return {"status": "success", "message": f"Successfully deleted deposition {deposition_id}"}
        else:
            return {"status": "failure", "message": f"Failed to delete deposition {deposition_id}"}

    def get_doi(self, deposition_id: int) -> str:
        """
        Simulate retrieving the DOI for a deposition (from the Fakenodo API).
        """
        deposition = self.get_deposition(deposition_id)
        return deposition.get("doi")  # Mock DOI returned by fakenodo
