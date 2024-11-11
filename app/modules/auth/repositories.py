from app.modules.auth.models import User, SignUpVerificationToken, ResetPasswordVerificationToken
from core.repositories.BaseRepository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    def create(self, commit: bool = True, **kwargs):
        password = kwargs.pop("password", None)  # Usa None como valor predeterminado
        instance = self.model(**kwargs)
        
        # Solo establece la contraseña si no es None
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

    def get_by_github_id(self, github_id):
        return User.query.filter_by(github_id=github_id).first()

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
