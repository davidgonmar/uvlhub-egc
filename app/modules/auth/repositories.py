from app.modules.auth.models import User, SignUpVerificationToken, ResetPasswordVerificationToken
from core.repositories.BaseRepository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    def create(self, commit: bool = True, **kwargs):
        # Extrae la contraseña solo si existe, ya que podría no estar presente en usuarios de Google
        password = kwargs.pop("password", None)
        instance = self.model(**kwargs)

        # Si se proporciona una contraseña, establece la contraseña
        if password:
            instance.set_password(password)
        
        self.session.add(instance)
        if commit:
            self.session.commit()
        else:
            self.session.flush()
        return instance

    def get_by_email(self, email: str):
        return self.model.query.filter_by(email=email).first()
    
    def get_by_orcid_id(self, orcid_id: str):
        return self.model.query.filter_by(orcid_id=orcid_id).first()


    def get_by_google_id(self, google_id: str):
        # Permite buscar usuarios mediante su Google ID
        return self.model.query.filter_by(google_id=google_id).first()


class SignUpVerificationTokenRepository(BaseRepository):
    def __init__(self):
        super().__init__(SignUpVerificationToken)

    def create(self, commit: bool = True, **kwargs) -> SignUpVerificationToken:
        instance = self.model(**kwargs)
        self.session.add(instance)
        if commit:
            self.session.commit()
        else:
            self.session.flush()
        return instance

    def get_by_email(self, email: str):
        return self.model.query.filter_by(email=email).first()

    def get_by_token(self, token: str):
        return self.model.query.filter_by(token=token).first()
    
    
class ResetPasswordVerificationTokenRepository(BaseRepository):
    def __init__(self):
        super().__init__(ResetPasswordVerificationToken)

    def create(self, commit: bool = True, **kwargs) -> ResetPasswordVerificationToken:
        instance = self.model(**kwargs)
        self.session.add(instance)
        if commit:
            self.session.commit()
        else:
            self.session.flush()
        return instance

    def get_by_email(self, email: str):
        return self.model.query.filter_by(email=email).first()

    def get_by_token(self, token: str):
        return self.model.query.filter_by(token=token).first()

