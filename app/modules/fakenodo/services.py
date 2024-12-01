import logging
import os
import uuid
import json
from flask import jsonify, Response
from flask_login import current_user
from app.modules.dataset.models import DataSet
from app.modules.fakenodo.repositories import FakenodoRepository
from app.modules.featuremodel.models import FeatureModel
from core.services.BaseService import BaseService

logger = logging.getLogger(__name__)

class FakenodoService(BaseService):
    
    def __init__(self):
        super().__init__(FakenodoRepository())
        # Initialize depositions as a dictionary to store the deposition data
        self.depositions = {}
        
    def _generate_deposition_id(self):
        """Generate a unique fake deposition ID."""
        return str(uuid.uuid4())

    def _generate_doi(self, deposition_id):
        """Generate a fake DOI based on the deposition ID."""
        return f"10.5281/fakenodo.{deposition_id}"

    def test_connection(self) -> bool:
        """
        Test the connection with Fakenodo (simulated success).
        """
        # In a real-world scenario, you would check if the API is up.
        return True

    def create_new_deposition(self, dataset: DataSet) -> dict:
        """
        Simulate creating a new deposition in Fakenodo.
        """
        deposition_id = self._generate_deposition_id()
        fake_doi = self._generate_doi(deposition_id)

        deposition_metadata = {
            "title": dataset.ds_meta_data.title,
            "description": dataset.ds_meta_data.description,
            "creators": [
                {
                    "name": author.name,
                    **({"affiliation": author.affiliation} if author.affiliation else {}),
                    **({"orcid": author.orcid} if author.orcid else {}),
                }
                for author in dataset.ds_meta_data.authors
            ],
            "keywords": dataset.ds_meta_data.tags.split(", ") if dataset.ds_meta_data.tags else [],
            "access_right": "open",
            "license": "CC-BY-4.0",
            "doi": fake_doi,
        }

        # Store the deposition data locally
        self.depositions[deposition_id] = {
            "metadata": deposition_metadata,
            "files": [],
            "published": False,
        }

        return {
            "deposition_id": deposition_id,
            "doi": fake_doi,
            "metadata": deposition_metadata
        }

    def upload_file(self, dataset: DataSet, deposition_id: str, feature_model: FeatureModel, user=None) -> dict:
        """
        Simulate uploading a file to a deposition and return detailed file metadata.
        """
        if deposition_id not in self.depositions:
            raise Exception("Deposition not found.")

        file_name = feature_model.fm_meta_data.uvl_filename
        file_path = os.path.join("uploads", f"user_{str(current_user.id)}", f"dataset_{dataset.id}", file_name)

        # Simulate saving the file in local storage
        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                f.write("Simulated file content.")

        # Add the file to the deposition's local record
        self.depositions[deposition_id]["files"].append(file_name)

        # Simulate file metadata similar to what Zenodo might return
        file_metadata = {
            "file_name": file_name,
            "file_size": os.path.getsize(file_path),
            "file_url": f"/uploads/user_{current_user.id}/dataset_{dataset.id}/{file_name}",
            "upload_time": "2024-12-01T12:00:00",  # Simulate a timestamp
        }

        return {
            "message": f"File {file_name} uploaded successfully.",
            "file_metadata": file_metadata
        }


    def publish_deposition(self, deposition_id: str) -> dict:
        """
        Simulate publishing a deposition.
        """
        if deposition_id not in self.depositions:
            raise Exception("Deposition not found.")
        
        # Simulate publishing by setting the 'published' status to True
        self.depositions[deposition_id]["published"] = True

        return {"message": "Deposition published successfully."}

    def get_deposition(self, deposition_id: str) -> dict:
        """
        Retrieve a deposition's details from Fakenodo.
        """
        if deposition_id not in self.depositions:
            raise Exception("Deposition not found.")

        return self.depositions[deposition_id]

    def get_doi(self, deposition_id: str) -> str:
        """
        Simulate getting a DOI for a deposition.
        
        If the DOI is not already generated, we will create one and store it in the deposition metadata.
        """
        if deposition_id not in self.depositions:
            raise Exception(f"Deposition with ID {deposition_id} not found.")
        
        # Check if DOI is already assigned, otherwise generate one
        deposition_metadata = self.depositions[deposition_id]["metadata"]
        if "doi" not in deposition_metadata:
            # Simulate DOI generation (format: 10.xxxx/yyyyyy)
            # You could use UUID or the dataset ID to make the DOI unique
            generated_doi = self.generate_doi(deposition_id)
            deposition_metadata["doi"] = generated_doi
        
        return deposition_metadata["doi"]

    def generate_doi(self, deposition_id: str) -> str:
        """
        Generate a unique DOI based on a predefined prefix and deposition ID.
        This simulates DOI generation for the dataset.
        """
        prefix = "10.5281"  # Example prefix (Zenodo's prefix is 10.5281)
        suffix = str(uuid.uuid5(uuid.NAMESPACE_DNS, deposition_id))  # Generate unique suffix from deposition ID
        return f"{prefix}/{suffix}"

    def get_all_depositions(self) -> dict:
        """
        Get all depositions from Fakenodo.
        """
        return self.depositions

    def delete_deposition(self, deposition_id: str) -> dict:
        """
        Simulate deleting a deposition from Fakenodo.
        """
        if deposition_id not in self.depositions:
            raise Exception("Deposition not found.")

        # Simulate deletion
        del self.depositions[deposition_id]

        return {"message": "Deposition deleted successfully."}
