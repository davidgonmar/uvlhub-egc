import logging
import os

from flask_login import current_user
from app.modules.dataset.models import DataSet
from app.modules.fakenodo.repositories import FakenodoRepository
from app.modules.featuremodel.models import FeatureModel
from core.services.BaseService import BaseService

logger = logging.getLogger(__name__)

class FakenodoService(BaseService):

    def __init__(self):
        self.deposition_repository = FakenodoRepository()
        # Initialize depositions as a dictionary to store the deposition data

    def _generate_doi(self, deposition_id):
        """Generate a fake DOI based on the deposition ID."""
        return f"10.5281/dataset{deposition_id}"

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
        deposition_id = dataset.id  # Use dataset's existing ID as deposition ID

        # Generate DOI based on the deposition ID
        fake_doi = self._generate_doi(deposition_id)

        # Prepare deposition metadata
        dep_metadata = {
            "title": dataset.ds_meta_data.title,
            "upload_type": "dataset" if dataset.ds_meta_data.publication_type.value == "none" else "publication",
            "publication_type": (
                dataset.ds_meta_data.publication_type.value
                if dataset.ds_meta_data.publication_type.value != "none"
                else None
            ),
            "description": dataset.ds_meta_data.description,
            "creators": [
                {
                    "name": author.name,
                    **({"affiliation": author.affiliation} if author.affiliation else {}),
                    **({"orcid": author.orcid} if author.orcid else {}),
                }
                for author in dataset.ds_meta_data.authors
            ],
            "keywords": (
                ["uvlhub"] if not dataset.ds_meta_data.tags else dataset.ds_meta_data.tags.split(", ") + ["uvlhub"]
            ),
            "access_right": "open",
            "license": "CC-BY-4.0"
        }

        # Store the DOI and metadata in the repository
        deposition = self.deposition_repository.create_new_deposition(fake_doi, dep_metadata)

        return {
            "deposition_id": deposition.id,  # ID from the repository
            "doi": fake_doi,
            "dep_metadata": dep_metadata,
            "message": "Deposition successfully created in Fakenodo"
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
        # Assuming depositions are stored in a dictionary or similar structure
        deposition = self.depositions.get(deposition_id)

        if not deposition:
            # Raise an error if the deposition with the provided ID is not found
            raise Exception(f"Deposition with ID {deposition_id} not found.")
        
        try:
            # Simulate generating a DOI for the deposition
            deposition["doi"] = f"fakenodo.doi.{deposition_id}"
            deposition["status"] = "published"  # Mark the deposition as published
            
            # Update the deposition in your storage (e.g., database or dictionary)
            self.depositions[deposition_id] = deposition

            # Return a success response with the deposition details
            response = {
                "id": deposition_id,
                "status": "published",
                "conceptdoi": deposition["doi"],  # Use the generated DOI here
                "message": "Deposition published successfully in Fakenodo."
            }
            return response

        except Exception as error:
            # Handle any errors that occur during the process and raise a new exception
            raise Exception(f"Failed to publish deposition with error: {str(error)}")


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
            generated_doi = self._generate_doi(deposition_id)
            deposition_metadata["doi"] = generated_doi
        
        return deposition_metadata["doi"]


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
