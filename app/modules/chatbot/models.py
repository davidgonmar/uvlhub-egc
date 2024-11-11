from app import db


class Chatbot(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f'Chatbot<{self.id}>'
