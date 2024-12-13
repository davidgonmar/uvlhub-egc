from datetime import datetime, timedelta, timezone
import os
import pytest
from flask import url_for, Flask

from app.modules.auth.services import AuthenticationService
from app.modules.auth.repositories import UserRepository, SignUpVerificationTokenRepository
from app.modules.profile.repositories import UserProfileRepository
import flask_login.utils
from unittest.mock import patch, MagicMock
from app.modules.auth.models import User
from app.modules.auth.repositories import ResetPasswordVerificationTokenRepository


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


@pytest.fixture
def invalid_token():
    return "token_invalido"


# LOGIN TESTS


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


# SIGNUP TESTS


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
    assert response.request.path == url_for("auth.show_signup_form"), "Signup was unsuccessful"


# Service tests

def test_service_create_with_profile_success(clean_database):
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


# Sign up code validation tests


def test_signup_code_validation_no_code(test_client):
    response = test_client.post(
        "/signup/code-validation",
        data=dict(code=""),
        follow_redirects=True
    )
    assert response.request.path == url_for("auth.validate_code"), "Signup code validation was unsuccessful"
    assert b"This field is required" in response.data, response.data


def test_signup_code_unsuccessful(test_client):
    wrong_code = "wrong"
    response = test_client.post(
        "/signup/code-validation",
        data=dict(code=wrong_code),
        follow_redirects=True,
    )
    assert response.request.path == url_for("auth.validate_code"), "Signup code validation was unsuccessful"


def test_service_create_code_succesful(clean_database):
    email = "service_test@example.com"

    AuthenticationService().generate_signup_verification_token(email)

    assert SignUpVerificationTokenRepository().count() == 1


def test_service_create_code_user_already_with_code(clean_database):
    email = "service_test@example.com"

    AuthenticationService().generate_signup_verification_token(email)
    AuthenticationService().generate_signup_verification_token(email)

    assert SignUpVerificationTokenRepository().count() == 1


def test_service_verify_code_no_code(clean_database):
    email = "service_test@example.com"
    fake_code = None

    acceptance = AuthenticationService().validate_signup_verification_token(email, fake_code)

    assert SignUpVerificationTokenRepository().count() == 0
    assert not acceptance


def test_service_verify_code_user_with_no_code(clean_database):
    email = "service_test@example.com"
    fake_code = "wrong"

    acceptance = AuthenticationService().validate_signup_verification_token(email, fake_code)

    assert SignUpVerificationTokenRepository().count() == 0
    assert not acceptance


def test_service_verify_code_outdated(clean_database):
    email = "service_test@example.com"
    MAX_VERIFICATION_TOKEN_AGE = AuthenticationService().get_max_verification_token_age()
    current_date = datetime.now(timezone.utc)
    outdated_date = current_date - timedelta(seconds=(MAX_VERIFICATION_TOKEN_AGE+1))
    data = {
        "email": email,
        "token": "whatever",
        "created_at": outdated_date
    }

    token_repository = SignUpVerificationTokenRepository()
    token = token_repository.create(**data)
    acceptance = AuthenticationService().validate_signup_verification_token(email, token)

    assert SignUpVerificationTokenRepository().count() == 0
    assert not acceptance


def test_service_verify_code_wrong_code(clean_database):
    email = "service_test@example.com"
    wrong_code = "false_code"

    AuthenticationService().generate_signup_verification_token(email)
    acceptance = AuthenticationService().validate_signup_verification_token(email, wrong_code)

    assert SignUpVerificationTokenRepository().count() == 1
    assert not acceptance


def test_service_verify_code_succesful(clean_database):
    email = "service_test@example.com"

    true_code = AuthenticationService().generate_signup_verification_token(email)
    acceptance = AuthenticationService().validate_signup_verification_token(email, true_code)

    assert SignUpVerificationTokenRepository().count() == 0
    assert acceptance
    assert UserProfileRepository().count() == 0


# Reset password tests

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
    mock_token_instance.id = 1
    mock_repo.get_by_email.return_value = mock_token_instance

    auth_service.rp_token_repository = mock_repo

    is_valid = auth_service.validate_resetpassword_verification_token(valid_email, token)

    assert is_valid is True

    mock_repo.delete.assert_called_once_with(mock_token_instance)

    mock_repo.get_by_email.return_value = None
    token_instance = mock_repo.get_by_email(valid_email)
    assert token_instance is None


def test_validate_resetpassword_verification_invalid_token(auth_service, valid_email, invalid_token):
    mock_repo = MagicMock()

    token = auth_service.generate_resetpassword_verification_token(valid_email)

    mock_token_instance = MagicMock()
    mock_token_instance.token = token
    mock_token_instance.created_at = datetime.now(timezone.utc)
    mock_repo.get_by_email.return_value = mock_token_instance

    auth_service.rp_token_repository = mock_repo

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


def test_generate_resetpassword_verification_token_replace_old(auth_service, valid_email, invalid_token):
    mock_repo = MagicMock()

    mock_token_instance = MagicMock()
    mock_token_instance.token = invalid_token
    mock_token_instance.created_at = datetime.now(timezone.utc) - timedelta(minutes=5)
    mock_token_instance.id = 1
    mock_repo.get_by_email.return_value = mock_token_instance

    auth_service.rp_token_repository = mock_repo

    new_token = auth_service.generate_resetpassword_verification_token(valid_email)

    assert new_token != invalid_token

    mock_repo.delete.assert_called_once_with(mock_token_instance.id)

    mock_repo.create.assert_called_once_with(email=valid_email, token=new_token)


# Redirection tests


def test_forgot_password_route_authenticated_user_redirect(test_client):
    mock_user = MagicMock()
    mock_user.is_authenticated = True

    with patch.object(flask_login.utils, "_get_user", return_value=mock_user):
        response = test_client.get("/forgotpassword/")
        assert response.status_code == 302
        assert response.headers["Location"] == "/"


# Reset password tests routes


def test_forgot_password_route_unregistered_email(test_client):
    mock_auth_service = MagicMock()
    mock_auth_service.is_email_available.return_value = True
    with patch("app.modules.auth.routes.authentication_service", mock_auth_service):
        response = test_client.post("/forgotpassword/", data={"email": "nonexistent@example.com"})

        mock_auth_service.is_email_available.assert_called_once_with("nonexistent@example.com")
        assert b"The email address nonexistent@example.com is not registered." in response.data
        assert response.status_code == 200


def test_forgot_password_route_sends_otp_successfully(test_client):
    mock_auth_service = MagicMock()
    mock_auth_service.is_email_available.return_value = False
    mock_auth_service.generate_resetpassword_verification_token.return_value = "123456"

    mock_email_service = MagicMock()

    with patch("app.modules.auth.routes.authentication_service", mock_auth_service), \
         patch("app.modules.auth.routes.email_service", mock_email_service):
        response = test_client.post("/forgotpassword/", data={"email": "test@example.com"})
        mock_auth_service.generate_resetpassword_verification_token.assert_called_once_with("test@example.com")
        mock_email_service.send_mail.assert_called_once_with(
            "test@example.com",
            "Your OTP code is: 123456. Please use this to reset your password.",
            "Password Reset OTP"
        )
        with test_client.session_transaction() as session:
            assert session['temp_user_data']['email'] == "test@example.com"
        assert response.status_code == 200
        assert b'<form' in response.data


def test_forgot_password_email_route_send_failure(test_client):
    """Verifica que se maneje un error al enviar el correo."""
    mock_auth_service = MagicMock()
    mock_auth_service.is_email_available.return_value = False
    mock_auth_service.generate_resetpassword_verification_token.return_value = "123456"

    mock_email_service = MagicMock()
    mock_email_service.send_mail.side_effect = Exception("SMTP error")

    with patch("app.modules.auth.routes.authentication_service", mock_auth_service), \
         patch("app.modules.auth.routes.email_service", mock_email_service):
        response = test_client.post("/forgotpassword/", data={"email": "user@example.com"})
        assert response.status_code == 200
        assert b"Error sending OTP: SMTP error" in response.data


def test_forgot_password_route_invalid_form(test_client):
    """Verifica que se muestre la plantilla inicial cuando el formulario no es válido."""
    mock_auth_service = MagicMock()
    mock_auth_service.is_email_available.return_value = False
    mock_auth_service.generate_resetpassword_verification_token.return_value = "123456"

    mock_email_service = MagicMock()
    with patch("app.modules.auth.routes.authentication_service", mock_auth_service), \
         patch("app.modules.auth.routes.email_service", mock_email_service):
        response = test_client.post("/forgotpassword/", data={"email": ""})
        assert response.status_code == 200
        assert b'Forgot your password?' in response.data
        assert b'<form' in response.data
        assert b'name="email"' in response.data


# forgot password code -validation tests


def test_code_validation_authenticated_user_redirect(test_client):
    """Verifica que los usuarios autenticados sean redirigidos al home"""
    mock_user = MagicMock()
    mock_user.is_authenticated = True

    with patch.object(flask_login.utils, "_get_user", return_value=mock_user):
        response = test_client.get("/forgotpassword/code-validation")
        assert response.status_code == 302
        assert response.headers["Location"] == "/"


def test_code_validation_route_invalid_otp(test_client):
    """Verifica que se muestre un error si el código OTP es inválido"""
    mock_auth_service = MagicMock()
    mock_auth_service.validate_resetpassword_verification_token.return_value = False

    with patch("app.modules.auth.routes.authentication_service", mock_auth_service):
        with test_client.session_transaction() as session:
            session['temp_user_data'] = {'email': 'user@example.com'}
        response = test_client.post("/forgotpassword/code-validation", data={"code": "654321"})
        assert response.status_code == 200
        assert b'<form' in response.data
        assert b'action="/forgotpassword/code-validation"' in response.data
        assert b"Invalid OTP code. Please try again." in response.data


def test_code_validation_success_otp(test_client):
    """Verifica que el código OTP correcto permite avanzar al formulario de restablecimiento de contraseña"""
    mock_auth_service = MagicMock()
    mock_auth_service.validate_resetpassword_verification_token.return_value = True

    with patch("app.modules.auth.routes.authentication_service", mock_auth_service):
        with test_client.session_transaction() as session:
            session['temp_user_data'] = {'email': 'user@example.com'}

        response = test_client.post("/forgotpassword/code-validation", data={"code": "123456"})
        assert response.status_code == 200
        assert b'<form' in response.data
        assert b'action="/resetpassword/"' in response.data
        assert b'name="password"' in response.data
        assert b'name="confirm_password"' in response.data


def test_code_validation_exception_handling(test_client):
    """Verifica que se maneje correctamente una excepción durante la validación del OTP"""
    mock_auth_service = MagicMock()
    mock_auth_service.validate_resetpassword_verification_token.side_effect = Exception("Unexpected error")

    with patch("app.modules.auth.routes.authentication_service", mock_auth_service):
        with test_client.session_transaction() as session:
            session['temp_user_data'] = {'email': 'user@example.com'}

        response = test_client.post("/forgotpassword/code-validation", data={"code": "123456"})

        assert response.status_code == 200
        assert b'<form' in response.data
        assert b'action="/forgotpassword/code-validation"' in response.data
        assert b"Error validating OTP: Unexpected error" in response.data


def test_code_validation_form_invalid(test_client):
    """Verifica que si el formulario no es válido, se muestre el formulario inicial sin errores adicionales"""
    mock_auth_service = MagicMock()

    with patch("app.modules.auth.routes.authentication_service", mock_auth_service):
        response = test_client.post("/forgotpassword/code-validation", data={})

        assert response.status_code == 200

        assert b'<form' in response.data
        assert b'action="/forgotpassword/code-validation"' in response.data

        assert b"Invalid OTP code" not in response.data
        assert b"Invalid session data" not in response.data
        assert b"Error validating OTP" not in response.data


def test_code_validation_no_temp_user_data(test_client):
    """Verifica que se muestre un error si la sesión no tiene datos de usuario temporal (`temp_user_data`)."""
    mock_auth_service = MagicMock()

    with patch("app.modules.auth.routes.authentication_service", mock_auth_service):
        with test_client.session_transaction() as session:
            session.clear()
        response = test_client.post("/forgotpassword/code-validation", data={"code": "123456"})

        assert response.status_code == 200
        assert b'<form' in response.data
        assert b'action="/forgotpassword/code-validation"' in response.data
        assert any(
            error_message in response.data
            for error_message in [
                b"Invalid session data",
                b"did not find temp_user_data"
            ]
        )

# reset password route tests


def test_reset_password_no_temp_user_data(test_client):
    """Verifica que se muestre un error si la sesión no tiene datos de usuario temporal (`temp_user_data`)."""
    with test_client.session_transaction() as session:
        session.clear()

    response = test_client.post(
        "/resetpassword/",
        data={"password": "newpassword", "confirm_password": "newpassword"}
    )
    assert response.status_code == 200
    assert b"Invalid session data: did not find temp_user_data" in response.data


def test_reset_password_passwords_do_not_match(test_client):
    """Verifica que se muestre un error si las contraseñas no coinciden."""
    with test_client.session_transaction() as session:
        session['temp_user_data'] = {'email': 'test@example.com'}

    response = test_client.post(
        "/resetpassword/",
        data={"password": "newpassword", "confirm_password": "differentpassword"}
    )
    assert response.status_code == 200
    assert b"Passwords do not match." in response.data


def test_reset_password_successful(test_client):
    """Verifica que la contraseña se restablezca correctamente."""
    mock_auth_service = MagicMock()
    with patch("app.modules.auth.routes.authentication_service", mock_auth_service):
        with test_client.session_transaction() as session:
            session['temp_user_data'] = {'email': 'test@example.com'}
        response = test_client.post("/resetpassword/", data={"password": "newpassword", "confirm_password": "newpassword"})
        mock_auth_service.reset_password.assert_called_once_with("test@example.com", "newpassword")
        assert response.status_code == 302
        assert response.headers["Location"] == "/"


def test_reset_password_error(test_client):
    """Verifica que se maneje un error al restablecer la contraseña."""
    mock_auth_service = MagicMock()
    mock_auth_service.reset_password.side_effect = Exception("Unexpected error")
    with patch("app.modules.auth.routes.authentication_service", mock_auth_service):
        with test_client.session_transaction() as session:
            session['temp_user_data'] = {'email': 'test@example.com'}

        response = test_client.post(
            "/resetpassword/",
            data={"password": "newpassword", "confirm_password": "newpassword"})
        assert response.status_code == 200
        assert b"Error resetting password: Unexpected error" in response.data


def test_reset_password_authenticated_user_redirect(test_client):
    """Verifica que los usuarios autenticados sean redirigidos al intentar acceder a la ruta de restablecimiento de contraseña."""
    mock_user = MagicMock()
    mock_user.is_authenticated = True
    with patch("flask_login.utils._get_user", return_value=mock_user):
        response = test_client.get("/resetpassword/")

        assert response.status_code == 302
        assert response.headers["Location"] == "/"


def test_reset_password_form_render_initial(test_client):
    """Verifica que la plantilla de restablecimiento de contraseña se renderice correctamente en una solicitud GET."""
    response = test_client.get("/resetpassword/")

    assert response.status_code == 200
    assert b'<form' in response.data
    assert b'name="password"' in response.data
    assert b'name="confirm_password"' in response.data

# MULTIPLE LOGIN TESTS

# ORCID

def test_configure_oauth():
    app = Flask(__name__)
    oauth_service = AuthenticationService()
    oauth, orcid = oauth_service.configure_oauth(app)

    assert oauth is not None
    assert orcid is not None
    assert orcid.client_id == oauth_service.client_id
    assert orcid.client_secret == oauth_service.client_secret
    assert orcid.access_token_url == 'https://orcid.org/oauth/token'
    assert orcid.authorize_url == 'https://orcid.org/oauth/authorize'

def test_get_orcid_full_profile_success():
    orcid_id = '0000-0001-2345-6789'
    token = {'access_token': 'mock_access_token'}

    orcid_service = AuthenticationService()

    # Mock
    mock_response = MagicMock()
    mock_response.ok = True
    mock_response.json.return_value = {
        'activities-summary': {
            'employments': {
                'affiliation-group': [{
                    'summaries': [{
                        'employment-summary': {
                            'organization': {'name': 'Test University'}
                        }
                    }]
                }]
            }
        },
        'person': {'emails': {'email': [{'email': 'test@example.com'}]}}
    }

    with patch.object(orcid_service.orcid_client, 'get', return_value=mock_response):
        full_profile = orcid_service.get_orcid_full_profile(orcid_id, token)

    assert full_profile['activities-summary']['employments']['affiliation-group'][0]['summaries'][0]['employment-summary']['organization']['name'] == 'Test University'
    assert full_profile['person']['emails']['email'][0]['email'] == 'test@example.com'

def test_orcid_login_route(test_client):
    response = test_client.get('/orcid/login')
    
    assert response.status_code == 302
    assert 'Location' in response.headers
    assert 'https://orcid.org/oauth/authorize' in response.headers['Location']


def test_orcid_authorize_route_invalid_access(test_client):
    response = test_client.get('/orcid/authorize')

    assert response.status_code == 400

# GOOGLE

def test_user_creation_with_google_success(clean_database):
    google_user_info = {
        "email": "test@example.com",
        "sub": "1234",
        "given_name": "Test",
        "family_name": "Foo"
    }

    user = AuthenticationService().get_or_create_user(google_user_info)

    # 1 usuario creado
    assert UserRepository().count() == 1
    assert UserProfileRepository().count() == 1

    # info de user = info de google
    assert user.email == google_user_info["email"]
    assert user.google_id == google_user_info["sub"]

    user_profile = user.profile  

    # perfil bien creado
    assert user_profile is not None, "El perfil del usuario no fue creado"
    assert user_profile.name == google_user_info["given_name"]
    assert user_profile.surname == google_user_info["family_name"]

    # asociación entre user y profile
    assert user_profile.user_id == user.id

def test_user_exists_with_google_data(clean_database):
    google_user_info = {
        "email": "existing_user@example.com",
        "sub": "1234",
        "given_name": "Jane",
        "family_name": "Smith"
    }

    # crea el user
    AuthenticationService().get_or_create_user(google_user_info)

    # intenta crear el mismo user
    user = AuthenticationService().get_or_create_user(google_user_info)

    # al existir, hace un get
    assert UserRepository().count() == 1
    assert UserProfileRepository().count() == 1

    # la info es la misma
    assert user.email == google_user_info["email"]
    assert user.google_id == google_user_info["sub"]

def test_user_creation_with_missing_google_data_error(clean_database):
    google_user_info = {
        "given_name": "Alice",
        "family_name": "Wonderland"
    }

    try:
        AuthenticationService().get_or_create_user(google_user_info)
        assert False, "Se esperaba un error debido a los datos incompletos"
    except ValueError as e:
        assert str(e) == "Email and google_id are required from Google user info."

def test_google_login_redirect(test_client):
    if os.environ.get("GITHUB_ACTIONS"):  # Solo para GitHub Actions
        pytest.skip("Skipping test due to external dependencies")

    response = test_client.get(url_for('auth.google_login'))
    assert response.status_code == 302
    assert "https://accounts.google.com/o/oauth2/auth" in response.location

#GITHUB

def test_user_creation_from_github_success(clean_database):
    github_user_info = {
        "github_id": "github_user_123",
        "github_email": "github_user_123@example.com",
        "name": "GitHub",
        "surname": "User"
    }

    user = AuthenticationService().get_or_create_user_from_github(
        github_user_info["github_id"],
        github_user_info["github_email"],
        github_user_info["name"],
        github_user_info["surname"]
    )

    assert UserRepository().count() == 1
    assert UserProfileRepository().count() == 1

    assert user.email == github_user_info["github_email"]
    assert user.github_id == github_user_info["github_id"]

    user_profile = user.profile
    assert user_profile is not None
    assert user_profile.name == github_user_info["name"]
    assert user_profile.surname == github_user_info["surname"]

def test_user_creation_from_github_with_default_values(clean_database):
    github_user_info = {
        "github_id": "github_user_124",
        "github_email": "github_user_124@example.com"
    }

    user = AuthenticationService().get_or_create_user_from_github(
        github_user_info["github_id"],
        github_user_info["github_email"]
    )

    assert UserRepository().count() == 1
    assert UserProfileRepository().count() == 1

    assert user.email == github_user_info["github_email"]
    assert user.github_id == github_user_info["github_id"]

    user_profile = user.profile
    assert user_profile is not None
    assert user_profile.name == "Default Name"
    assert user_profile.surname == "Default Surname"

def test_user_creation_from_github_with_missing_email(clean_database):
    github_user_info = {
        "github_id": "github_user_125",
        "name": "GitHub",
        "surname": "User"
    }

    user = AuthenticationService().get_or_create_user_from_github(
        github_user_info["github_id"],
        github_email=None,
        name=github_user_info["name"],
        surname=github_user_info["surname"]
    )

    assert UserRepository().count() == 1
    assert UserProfileRepository().count() == 1

    assert user.email == "user_github_user_125@example.com"  # default value based on github_id

def test_user_creation_from_github_with_duplicate_github_id(clean_database):
    github_user_info1 = {
        "github_id": "github_user_126",
        "github_email": "github_user_126@example.com",
        "name": "First",
        "surname": "User"
    }

    github_user_info2 = {
        "github_id": "github_user_126",
        "github_email": "another_user@example.com",
        "name": "Second",
        "surname": "User"
    }

    # 1er user
    AuthenticationService().get_or_create_user_from_github(
        github_user_info1["github_id"],
        github_user_info1["github_email"],
        github_user_info1["name"],
        github_user_info1["surname"]
    )

    # 2o user
    user = AuthenticationService().get_or_create_user_from_github(
        github_user_info2["github_id"],
        github_user_info2["github_email"],
        github_user_info2["name"],
        github_user_info2["surname"]
    )

    # solo 1 creado
    assert UserRepository().count() == 1
    assert UserProfileRepository().count() == 1

    # 1er usuario devuelto
    assert user.github_id == github_user_info1["github_id"]
    assert user.email == github_user_info1["github_email"]

def test_github_login_redirect(test_client):
    if os.environ.get("GITHUB_ACTIONS"):  # Solo para GitHub Actions
        pytest.skip("Skipping test due to external dependencies")

    response = test_client.get(url_for('auth.github_login'))

    assert response.status_code == 302
    assert "/github" in response.location
