from app import db

class Fakenodo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    def __repr__(self):
        return f'Fakenodo<{self.id}>'