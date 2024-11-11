from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=True)  # Ahora opcional para usuarios de GitHub
    github_id = db.Column(db.String(100), unique=True, nullable=True)  # Campo para ID de GitHub
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    
    data_sets = db.relationship('DataSet', backref='user', lazy=True)
    profile = db.relationship('UserProfile', backref='user', uselist=False)
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        # Configura la contraseña solo si se proporciona (usuarios de GitHub no tendrán una contraseña)
        if 'password' in kwargs and kwargs['password']:
            self.set_password(kwargs['password'])

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def temp_folder(self) -> str:
        from app.modules.auth.services import AuthenticationService
        return AuthenticationService().temp_folder_by_user(self)


class SignUpVerificationToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(256), nullable=False, unique=True) # only one token per email at a time
    token = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<SignUpVerificationToken {self.email}>'
    

class ResetPasswordVerificationToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(256), nullable=False, unique=True)
    token = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<ResetPasswordVerificationToken {self.email}>'