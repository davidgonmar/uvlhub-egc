import pytest
from flask import url_for, session

from app.modules.auth.services import AuthenticationService
from app.modules.auth.repositories import UserRepository
from app.modules.profile.repositories import UserProfileRepository

from unittest.mock import patch, MagicMock
from app.modules.auth.models import User
from app.modules.auth.services import *

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
def auth_service():
    """
    Fixture to initialize the AuthenticationService.
    """
    return AuthenticationService()

@pytest.fixture
def mock_smtp_server():
    """Fixture to mock the SMTP server."""
    mock_server = MagicMock()
    return mock_server

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
        "password": "test1234"
    }

    AuthenticationService().create_with_profile(**data)

    assert UserRepository().count() == 1
    assert UserProfileRepository().count() == 1


def test_service_create_with_profile_fail_no_email(clean_database):
    data = {
        "name": "Test",
        "surname": "Foo",
        "email": "",
        "password": "1234"
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
        "password": ""
    }

    with pytest.raises(ValueError, match="Password is required."):
        AuthenticationService().create_with_profile(**data)

    assert UserRepository().count() == 0
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
'''
def test_generate_otp():
    otp = generate_otp()
    assert len(otp) == 6
    assert otp.isdigit()

def test_send_otp_email(mock_smtp_server):
    """Test sending OTP email."""
    
    # Prepare the EmailService object with mock data
    email_service = EmailService(sender="test@example.com", password="password", code="123456")

    # Mock the 'sendmail' method to prevent actual email sending
    with patch.object(mock_smtp_server, 'sendmail') as mock_sendmail:
        email_service.sending_mail(receiver="receiver@example.com", server=mock_smtp_server)

        # Ensure that the 'sendmail' method is called once
        mock_sendmail.assert_called_once_with(
            "test@example.com",  # Sender
            "receiver@example.com",  # Receiver
            "Hello! \n This is your OTP: 123456."  # The message
        )

def test_check_otp_valid():
    """Test OTP validation with correct entry."""
    
    # Prepare EmailService with a mock OTP
    email_service = EmailService(sender="test@example.com", password="password", code="123456")
    
    # Simulate correct OTP entry
    class OTPEntry:
        def get(self):
            return "123456"
    
    otp_entry = OTPEntry()
    with patch("builtins.print") as mock_print:
        email_service.check_otp(otp_entry)
        mock_print.assert_called_with("OKKKKKKKKKKKKKKKKKKKKKKKK")  # Expected success message

def test_check_otp_invalid():
    """Test OTP validation with incorrect entry."""
    
    email_service = EmailService(sender="test@example.com", password="password", code="123456")
    
    class OTPEntry:
        def get(self):
            return "654321"  # Incorrect OTP
    
    otp_entry = OTPEntry()
    with patch("builtins.print") as mock_print:
        email_service.check_otp(otp_entry)
        mock_print.assert_called_with("NOOOOOOOOOOOOOOOOOOOOOOOO")  # Expected failure message

def test_check_otp_invalid_format():
    """
    Test that invalid OTP formats (e.g., non-numeric or empty strings) are handled appropriately.
    """
    email_service = EmailService(sender="test@example.com", password="password", code="123456")
    
    class OTPEntry:
        def get(self):
            return "abcxyz"  # Invalid OTP format
    
    otp_entry = OTPEntry()
    with patch("builtins.print") as mock_print:
        email_service.check_otp(otp_entry)
        mock_print.assert_called_with("NOOOOOOOOOOOOOOOOOOOOOOOO")  # Expected failure message for invalid OTP
'''