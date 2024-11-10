import os
from flask_login import login_user
from flask_login import current_user

from flask import current_app
from app import db
from authlib.integrations.flask_client import OAuth

from app.modules.auth.models import User
from app.modules.auth.repositories import UserRepository
from app.modules.profile.models import UserProfile
from app.modules.profile.repositories import UserProfileRepository
from core.configuration.configuration import uploads_folder_name
from core.services.BaseService import BaseService


class AuthenticationService(BaseService):
    def __init__(self):
        super().__init__(UserRepository())
        self.user_profile_repository = UserProfileRepository()
        self.client_id = os.getenv("ORCID_CLIENT_ID")
        self.client_secret = os.getenv("ORCID_CLIENT_SECRET")
        self.oauth, self.orcid_client = self.configure_oauth(current_app)

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
                "password": password
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

    def get_user_by_email(self, email: str) -> User | None:
        return self.repository.get_by_email(email)
    
    def reset_password(self, email: str, new_password: str) -> bool:
        user = self.get_user_by_email(email)
        if user is None:
            raise ValueError(f"User with email {email} does not exist.")

        user.set_password(new_password)
        self.repository.session.commit()

        return True
    
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
