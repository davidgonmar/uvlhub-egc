from app import db


class Fakenodo(db.Model):
    id = db.Column(db.Integer, primary_key=True)