from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    
    # Datos básicos
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=True)  # O puede ser nullable si no usas contraseña.
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    
    # Nuevo campo para el Google ID
    google_id = db.Column(db.String(256), unique=True, nullable=True)  # Para autenticar por Google
    
    # Relaciones con otros modelos
    data_sets = db.relationship('DataSet', backref='user', lazy=True)
    profile = db.relationship('UserProfile', backref='user', uselist=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if 'password' in kwargs and kwargs['password']:
            self.set_password(kwargs['password'])

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        if self.password:
            return check_password_hash(self.password, password)
        return False  # Si no hay contraseña, devolver False

    def temp_folder(self) -> str:
        from app.modules.auth.services import AuthenticationService
        return AuthenticationService().temp_folder_by_user(self)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    def get_id(self):
        return str(self.id)

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

