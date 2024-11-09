import os
from flask_login import login_user, current_user
from app.modules.auth.models import User
from app.modules.auth.repositories import UserRepository
from app.modules.profile.models import UserProfile
from app.modules.profile.repositories import UserProfileRepository
from core.configuration.configuration import uploads_folder_name
from core.services.BaseService import BaseService
from flask import current_app as app  # Importar el logger de Flask

class AuthenticationService(BaseService):
    def __init__(self):
        super().__init__(UserRepository())
        self.user_profile_repository = UserProfileRepository()

    def login(self, email, password, remember=True):
        user = self.repository.get_by_email(email)
        if user is not None and user.check_password(password):
            login_user(user, remember=remember)
            app.logger.info(f"User logged in: {user.email} - Authenticated: {current_user.is_authenticated}")  # Mejor usar logger
            return True
        app.logger.warning(f"Login failed for user: {email}")  # Log para cuando el login falla
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

            app.logger.info(f"User created: {user.email}")  # Log de usuario creado
        except Exception as exc:
            self.repository.session.rollback()
            app.logger.error(f"Error creating user: {exc}")  # Log de error
            raise exc
        return user

    def update_profile(self, user_profile_id, form):
        if form.validate():
            updated_instance = self.update(user_profile_id, **form.data)
            return updated_instance, None
        app.logger.warning(f"Profile update failed: {form.errors}")  # Log si el formulario tiene errores
        return None, form.errors

    def get_authenticated_user(self) -> User | None:
        if current_user.is_authenticated:
            app.logger.info(f"Authenticated user: {current_user.email}")  # Log de usuario autenticado
            return current_user
        app.logger.warning("No authenticated user found.")  # Log si no hay usuario autenticado
        return None

    def get_authenticated_user_profile(self) -> UserProfile | None:
        if current_user.is_authenticated:
            app.logger.info(f"Authenticated user profile: {current_user.profile.name}")  # Log del perfil
            return current_user.profile
        app.logger.warning("No authenticated user profile found.")  # Log si no hay perfil autenticado
        return None

    def temp_folder_by_user(self, user: User) -> str:
        return os.path.join(uploads_folder_name(), "temp", str(user.id))

    def get_or_create_user(self, google_user_info):
        app.logger.info(f"Google user info received: {google_user_info}")  # Log para ver la info del usuario de Google
        email = google_user_info.get("email")
        google_id = google_user_info.get("sub")  # Obtener google_id

        if not email or not google_id:
            raise ValueError("Email and google_id are required from Google user info.")

        # Primero intentar encontrar al usuario por google_id
        user = self.repository.get_by_google_id(google_id)

        if user:
            app.logger.info(f"User with Google ID {google_id} already exists: {user.email}")  # Log si el usuario ya existe
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

        app.logger.info(f"User created with Google ID: {user.email}")  # Log de usuario creado
        
        return user
    def get_user_by_email(self, email: str):
        # Buscar al usuario por email usando el repositorio
        return self.repository.get_by_email(email)