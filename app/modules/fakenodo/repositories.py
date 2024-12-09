from app.modules.fakenodo.models import Fakenodo
from core.repositories.BaseRepository import BaseRepository
from app import db

class FakenodoRepository(BaseRepository):
    def __init__(self):
        super().__init__(Fakenodo)  # Initialize with Fakenodo model

    def create_new_deposition(self, doi, dep_metadata):
        """Create a new deposition with a DOI and metadata."""
        # Ensure dep_metadata is not empty and passed to the Fakenodo model
        if dep_metadata is None:
            dep_metadata = {}  # Default empty dictionary if no metadata provided

        deposition = Fakenodo(doi=doi, dep_metadata=dep_metadata)
        db.session.add(deposition)
        db.session.commit()
        return deposition
