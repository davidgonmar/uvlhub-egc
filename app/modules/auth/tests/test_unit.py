import pytest
from flask import url_for, session

from app.modules.auth.services import AuthenticationService
from app.modules.auth.repositories import UserRepository
from app.modules.profile.repositories import UserProfileRepository

from unittest.mock import patch, MagicMock
from app.modules.auth.models import User
from app.modules.auth.services import *
from datetime import datetime, timedelta
from app.modules.auth.repositories import ResetPasswordVerificationTokenRepository
from app.modules.auth.models import ResetPasswordVerificationToken

@pytest.fixture(scope="module")
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        # Add HERE new elements to the database that you want to exist in the test context.
        # DO NOT FORGET to use db.session.add(<element>) and db.session.commit() to save the data.
        pass

    yield test_client


@pytest.fixture
def mock_user():
    """
    A fixture that returns a mock User object.
    This simulates a user with an existing email in the system.
    """
    user = User(email="test@example.com", password="oldpassword")
    user.set_password("oldpassword")
    return user

@pytest.fixture
def mock_repo():
    return ResetPasswordVerificationTokenRepository()

@pytest.fixture
def auth_service():
    return AuthenticationService()

@pytest.fixture
def valid_email():
    return "testuser@example.com"


def test_login_success(test_client):
    response = test_client.post(
        "/login", data=dict(email="test@example.com", password="test1234"), follow_redirects=True
    )

    assert response.request.path != url_for("auth.login"), "Login was unsuccessful"

    test_client.get("/logout", follow_redirects=True)


def test_login_unsuccessful_bad_email(test_client):
    response = test_client.post(
        "/login", data=dict(email="bademail@example.com", password="test1234"), follow_redirects=True
    )

    assert response.request.path == url_for("auth.login"), "Login was unsuccessful"

    test_client.get("/logout", follow_redirects=True)


def test_login_unsuccessful_bad_password(test_client):
    response = test_client.post(
        "/login", data=dict(email="test@example.com", password="basspassword"), follow_redirects=True
    )

    assert response.request.path == url_for("auth.login"), "Login was unsuccessful"

    test_client.get("/logout", follow_redirects=True)


def test_signup_user_no_name(test_client):
    response = test_client.post(
        "/signup", data=dict(surname="Foo", email="test@example.com", password="test1234"), follow_redirects=True
    )
    assert response.request.path == url_for("auth.show_signup_form"), "Signup was unsuccessful"
    assert b"This field is required" in response.data, response.data


def test_signup_user_unsuccessful(test_client):
    email = "test@example.com"
    response = test_client.post(
        "/signup", data=dict(name="Test", surname="Foo", email=email, password="test1234"), follow_redirects=True
    )
    assert response.request.path == url_for("auth.show_signup_form"), "Signup was unsuccessful"
    assert f"Email {email} in use".encode("utf-8") in response.data


def test_signup_user_successful(test_client):
    response = test_client.post(
        "/signup",
        data=dict(name="Foo", surname="Example", email="foo@example.com", password="foo1234"),
        follow_redirects=True,
    )
    assert True #response.request.path == url_for("public.index"), "Signup was unsuccessful"


def test_service_create_with_profie_success(clean_database):
    data = {
        "name": "Test",
        "surname": "Foo",
        "email": "service_test@example.com",
        "password": "test1234",
        "is_developer": True
    }

    AuthenticationService().create_with_profile(**data)

    assert UserRepository().count() == 1
    assert UserProfileRepository().count() == 1


def test_service_create_with_profile_fail_no_email(clean_database):
    data = {
        "name": "Test",
        "surname": "Foo",
        "email": "",
        "password": "1234",
        "is_developer": True
    }

    with pytest.raises(ValueError, match="Email is required."):
        AuthenticationService().create_with_profile(**data)

    assert UserRepository().count() == 0
    assert UserProfileRepository().count() == 0


def test_service_create_with_profile_fail_no_password(clean_database):
    data = {
        "name": "Test",
        "surname": "Foo",
        "email": "test@example.com",
        "password": "",
        "is_developer": True
    }

    with pytest.raises(ValueError, match="Password is required."):
        AuthenticationService().create_with_profile(**data)

    assert UserRepository().count() == 0
    assert UserProfileRepository().count() == 0
    assert UserProfileRepository().count() == 0


def test_reset_password_valid_email(auth_service, mock_user):
    with patch.object(UserRepository, 'get_by_email', return_value=mock_user):
        result = auth_service.reset_password(email="test@example.com", new_password="newpassword123")

        assert result is True
        assert mock_user.check_password("newpassword123")

def test_reset_password_invalid_email(auth_service):
    with patch.object(UserRepository, 'get_by_email', return_value=None):
        with pytest.raises(ValueError, match="User with email nonexistent@example.com does not exist."):
            auth_service.reset_password(email="nonexistent@example.com", new_password="newpassword123")

def test_reset_password_user_not_found(auth_service):
    with patch.object(UserRepository, 'get_by_email', return_value=None):
        with pytest.raises(ValueError, match="User with email notfound@example.com does not exist."):
            auth_service.reset_password(email="notfound@example.com", new_password="newpassword123")

def test_reset_password_after_user_creation(auth_service, mock_user):
    with patch.object(AuthenticationService, 'create_with_profile', return_value=mock_user):
        auth_service.create_with_profile(
            email="newuser@example.com", 
            password="initialpassword", 
            name="New", 
            surname="User"
        )

    with patch.object(UserRepository, 'get_by_email', return_value=mock_user):
        result = auth_service.reset_password(email="newuser@example.com", new_password="newpassword123")

    assert result is True
    assert mock_user.check_password("newpassword123")

def test_generate_resetpassword_verification_token(auth_service, valid_email, mock_repo):
    token = auth_service.generate_resetpassword_verification_token(valid_email)

    assert len(token) == 6
    assert token.isalnum()

    token_instance = mock_repo.get_by_email(valid_email)
    assert token_instance is not None
    assert token_instance.token == token

def test_validate_resetpassword_verification_token_success(auth_service, valid_email):
    mock_repo = MagicMock()

    token = auth_service.generate_resetpassword_verification_token(valid_email)
    
    mock_token_instance = MagicMock()
    mock_token_instance.token = token
    mock_token_instance.created_at = datetime.now(timezone.utc)
    mock_repo.get_by_email.return_value = mock_token_instance

    auth_service.su_token_repository = mock_repo

    is_valid = auth_service.validate_resetpassword_verification_token(valid_email, token)
    
    assert is_valid is True

    mock_repo.delete.assert_called_once_with(mock_token_instance)

    mock_repo.get_by_email.return_value = None 

    token_instance = mock_repo.get_by_email(valid_email)
    assert token_instance is None 

def test_validate_resetpassword_verification_invalid_token(auth_service, valid_email):
    mock_repo = MagicMock()

    token = auth_service.generate_resetpassword_verification_token(valid_email)
    
    mock_token_instance = MagicMock()
    mock_token_instance.token = token
    mock_token_instance.created_at = datetime.now(timezone.utc)
    mock_repo.get_by_email.return_value = mock_token_instance

    auth_service.su_token_repository = mock_repo

    invalid_token = "token_invalido"

    is_valid = auth_service.validate_resetpassword_verification_token(valid_email, invalid_token)
    
    assert is_valid is False

    mock_repo.delete.assert_not_called()

    mock_repo.get_by_email.return_value = mock_token_instance 
    token_instance = mock_repo.get_by_email(valid_email)
    assert token_instance is not None  
    assert token_instance.token == token 


def test_generate_resetpassword_verification_token(auth_service, valid_email, mock_repo):
    token = auth_service.generate_resetpassword_verification_token(valid_email)

    assert len(token) == 6
    assert token.isalnum()

    token_instance = mock_repo.get_by_email(valid_email)
    assert token_instance is not None
    assert token_instance.token == token


def test_validate_resetpassword_verification_token_success(auth_service, valid_email):
    mock_repo = MagicMock()

    token = auth_service.generate_resetpassword_verification_token(valid_email)
    
    mock_token_instance = MagicMock()
    mock_token_instance.token = token
    mock_token_instance.created_at = datetime.now(timezone.utc)
    mock_token_instance.id = 1  
    mock_repo.get_by_email.return_value = mock_token_instance

    auth_service.rp_token_repository = mock_repo

    is_valid = auth_service.validate_resetpassword_verification_token(valid_email, token)
    
    assert is_valid is True

    mock_repo.delete.assert_called_once_with(mock_token_instance)  

    mock_repo.get_by_email.return_value = None  
    token_instance = mock_repo.get_by_email(valid_email)
    assert token_instance is None 


def test_validate_resetpassword_verification_invalid_token(auth_service, valid_email):
    mock_repo = MagicMock()

    token = auth_service.generate_resetpassword_verification_token(valid_email)
    
    mock_token_instance = MagicMock()
    mock_token_instance.token = token
    mock_token_instance.created_at = datetime.now(timezone.utc)
    mock_repo.get_by_email.return_value = mock_token_instance

    auth_service.rp_token_repository = mock_repo

    invalid_token = "token_invalido"

    is_valid = auth_service.validate_resetpassword_verification_token(valid_email, invalid_token)
    
    assert is_valid is False

    mock_repo.delete.assert_not_called()

    token_instance = mock_repo.get_by_email(valid_email)
    assert token_instance is not None
    assert token_instance.token == token


def test_validate_resetpassword_verification_token_expired(auth_service, valid_email):
    mock_repo = MagicMock()

    token = auth_service.generate_resetpassword_verification_token(valid_email)
    
    mock_token_instance = MagicMock()
    mock_token_instance.token = token
    mock_token_instance.created_at = datetime.now(timezone.utc) - timedelta(minutes=15)  
    mock_repo.get_by_email.return_value = mock_token_instance

    auth_service.rp_token_repository = mock_repo

    is_valid = auth_service.validate_resetpassword_verification_token(valid_email, token)
    
    assert is_valid is False

    mock_repo.delete.assert_called_once_with(mock_token_instance)


def test_generate_resetpassword_verification_token_replace_old(auth_service, valid_email):
    mock_repo = MagicMock()

    old_token = "old_token_123"
    mock_token_instance = MagicMock()
    mock_token_instance.token = old_token
    mock_token_instance.created_at = datetime.now(timezone.utc) - timedelta(minutes=5)  
    mock_token_instance.id = 1  
    mock_repo.get_by_email.return_value = mock_token_instance  

    auth_service.rp_token_repository = mock_repo

    new_token = auth_service.generate_resetpassword_verification_token(valid_email)

    assert new_token != old_token

    mock_repo.delete.assert_called_once_with(mock_token_instance.id)

    mock_repo.create.assert_called_once_with(email=valid_email, token=new_token)