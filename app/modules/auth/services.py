import os

from flask_login import login_user, current_user

from flask import current_app as app
from authlib.integrations.flask_client import OAuth

from app.modules.auth.models import User
from app.modules.auth.repositories import UserRepository, SignUpVerificationTokenRepository
from app.modules.auth.repositories import ResetPasswordVerificationTokenRepository
from app.modules.profile.models import UserProfile
from app.modules.profile.repositories import UserProfileRepository
from core.configuration.configuration import uploads_folder_name
from core.services.BaseService import BaseService

import secrets
from datetime import datetime, timezone
import smtplib


MAX_VERIFICATION_TOKEN_AGE = 60 * 10  # 10 minutes


class AuthenticationService(BaseService):
    def __init__(self):
        super().__init__(UserRepository())
        self.user_profile_repository = UserProfileRepository()
        self.client_id = os.getenv("ORCID_CLIENT_ID")
        self.client_secret = os.getenv("ORCID_CLIENT_SECRET")
        self.oauth, self.orcid_client = self.configure_oauth(app)
        self.su_token_repository = SignUpVerificationTokenRepository()
        self.rp_token_repository = ResetPasswordVerificationTokenRepository()

    def generate_signup_verification_token(self, email: str) -> str:
        # there can only be one token per email at a time
        if token := self.su_token_repository.get_by_email(email):
            self.su_token_repository.delete(token.id)
        token = secrets.token_hex(3)  # 6 characters
        self.su_token_repository.create(email=email, token=token)
        return token

    def validate_signup_verification_token(self, email: str, token: str, delete=True) -> bool:
        token_instance = self.su_token_repository.get_by_email(email)
        if token_instance is None:
            return False
        now = datetime.now(timezone.utc).timestamp()
        created_at = token_instance.created_at.replace(tzinfo=timezone.utc).timestamp()
        if (now - created_at) > MAX_VERIFICATION_TOKEN_AGE:
            self.su_token_repository.delete(token_instance.id)
            return False
        if token_instance.token == token:
            (lambda: self.su_token_repository.delete(token_instance.id) if delete else lambda: None)()
            return True
        return False

    def generate_resetpassword_verification_token(self, email: str) -> str:
        if token := self.rp_token_repository.get_by_email(email):
            self.rp_token_repository.delete(token.id)
        token = secrets.token_hex(3)
        self.rp_token_repository.create(email=email, token=token)
        return token

    def validate_resetpassword_verification_token(self, email: str, token: str, delete=True) -> bool:
        token_instance = self.rp_token_repository.get_by_email(email)
        if token_instance is None:
            return False
        now = datetime.now(timezone.utc).timestamp()
        created_at = token_instance.created_at.replace(tzinfo=timezone.utc).timestamp()
        if (now - created_at) > MAX_VERIFICATION_TOKEN_AGE:
            self.rp_token_repository.delete(token_instance)
            return False
        if token_instance.token == token:
            (lambda: self.rp_token_repository.delete(token_instance) if delete else lambda: None)()
            return True
        return False

    def get_max_verification_token_age(self):
        return MAX_VERIFICATION_TOKEN_AGE

    def login(self, email, password, remember=True):
        user = self.repository.get_by_email(email)
        if user is not None and user.check_password(password):
            login_user(user, remember=remember)
            return True
        return False

    def is_email_available(self, email: str) -> bool:
        return self.repository.get_by_email(email) is None

    def create_with_profile(self, **kwargs):
        try:
            email = kwargs.pop("email", None)
            password = kwargs.pop("password", None)
            name = kwargs.pop("name", None)
            surname = kwargs.pop("surname", None)
            is_developer = kwargs.pop("is_developer", False)

            if not email:
                raise ValueError("Email is required.")
            if not password:
                raise ValueError("Password is required.")
            if not name:
                raise ValueError("Name is required.")
            if not surname:
                raise ValueError("Surname is required.")

            user_data = {
                "email": email,
                "password": password,
                "is_developer": is_developer
            }

            profile_data = {
                "name": name,
                "surname": surname,
            }

            user = self.create(commit=False, **user_data)
            profile_data["user_id"] = user.id
            self.user_profile_repository.create(**profile_data)
            self.repository.session.commit()
        except Exception as exc:
            self.repository.session.rollback()
            raise exc
        return user

    def update_profile(self, user_profile_id, form):
        if form.validate():
            updated_instance = self.update(user_profile_id, **form.data)
            return updated_instance, None
        return None, form.errors

    def get_authenticated_user(self) -> User | None:
        if current_user.is_authenticated:
            return current_user
        return None

    def get_authenticated_user_profile(self) -> UserProfile | None:
        if current_user.is_authenticated:
            return current_user.profile
        return None

    def temp_folder_by_user(self, user: User) -> str:
        return os.path.join(uploads_folder_name(), "temp", str(user.id))

    def get_or_create_user_from_github(self, github_id, github_email, name=None, surname=None):
        user = self.repository.get_by_github_id(github_id)
        if not user:
            print("Creating new user")

            if not github_email:
                github_email = f"user_{github_id}@example.com"  # O cualquier otra lógica que desees

            user_data = {
                "email": github_email,
                "github_id": github_id,
                "password": None  # Establece la contraseña como None
            }

            user = self.create(commit=False, **user_data)

            profile_data = {
                "name": name or "Default Name",  # Puedes usar un nombre por defecto o uno proporcionado
                "surname": surname or "Default Surname",  # Igualmente para el apellido
                "user_id": user.id
            }

            self.user_profile_repository.create(**profile_data)
            self.repository.session.commit()
        return user

    def get_user_by_email(self, email: str) -> User | None:
        return self.repository.get_by_email(email)

    def reset_password(self, email: str, new_password: str) -> bool:
        user = self.get_user_by_email(email)
        if user is None:
            raise ValueError(f"User with email {email} does not exist.")

        user.set_password(new_password)
        self.repository.session.commit()

        return True

    def get_or_create_user(self, google_user_info):
        email = google_user_info.get("email")
        google_id = google_user_info.get("sub")  # Obtener google_id

        if not email or not google_id:
            raise ValueError("Email and google_id are required from Google user info.")

        # Primero intentar encontrar al usuario por google_id
        user = self.repository.get_by_google_id(google_id)

        if user:
            return user

        # Si no existe, crear un nuevo usuario
        user_data = {
            "email": email,
            "google_id": google_id,  # Guardar google_id
            "password": ""  # No se usa contraseña para inicios de sesión sociales
        }

        user = self.create(commit=False, **user_data)  # Crear usuario sin confirmar en la base de datos
        self.repository.session.add(user)  # Agregar a la sesión

        profile_data = {
            "name": google_user_info.get("given_name", ""),
            "surname": google_user_info.get("family_name", ""),
        }
        profile_data["user_id"] = user.id
        self.user_profile_repository.create(**profile_data)  # Crear el perfil del usuario
        self.repository.session.commit()  # Confirmar los cambios

        return user

    def configure_oauth(self, app):
        oauth = OAuth(app)
        orcid = oauth.register(
            name='orcid',
            client_id=self.client_id,
            client_secret=self.client_secret,
            access_token_url='https://orcid.org/oauth/token',
            authorize_url='https://orcid.org/oauth/authorize',
            client_kwargs={
                'scope': '/authenticate',
                'token_endpoint_auth_method': 'client_secret_post'
            }
        )
        return oauth, orcid

    def get_orcid_full_profile(self, orcid_id, token):
        # Nota: La URL y la autorización deben estar correctos según la documentación y el alcance de ORCID
        url = f'https://pub.orcid.org/v3.0/{orcid_id}/record'
        headers = {
            'Authorization': f'Bearer {token["access_token"]}',
            'Accept': 'application/json'
        }
        resp = self.orcid_client.get(url, headers=headers)
        return resp.json() if resp.ok else {}


class EmailService():
    def __init__(self, sender: str, password: str):
        self.sender = sender
        self.password = password

    def send_mail(self, receiver: str, message: str, subject: str = ""):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.sender, self.password)
        msg = f'Subject: {subject}\n\n{message}'
        server.sendmail(self.sender, receiver, msg)
        server.quit()
