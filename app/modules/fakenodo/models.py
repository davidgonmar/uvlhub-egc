from app import db

class Fakenodo(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Deposition ID
    doi = db.Column(db.String(255), unique=True, nullable=False)  # DOI column
    dep_metadata = db.Column(db.JSON, nullable=True)  # Metadata column in JSON format

    def __init__(self, doi, dep_metadata):
        self.doi = doi
        self.metadata = dep_metadata

    def __repr__(self):
        return f"<Fakenodo(id={self.id}, doi={self.doi})>"
