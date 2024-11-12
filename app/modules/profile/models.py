from app import db


class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    orcid = db.Column(db.String(19), unique=True, nullable=True)
    affiliation = db.Column(db.String(100))
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    github = db.Column(db.String(39), nullable=True)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
