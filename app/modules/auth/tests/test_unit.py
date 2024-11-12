from datetime import datetime, timedelta, timezone
import pytest
from flask import url_for

from app.modules.auth.services import AuthenticationService
from app.modules.auth.repositories import UserRepository, SignUpVerificationTokenRepository
from app.modules.profile.repositories import UserProfileRepository


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
    assert response.request.path == url_for("auth.show_signup_form"), "Signup was unsuccessful"


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


def test_service_create_code_wrong_code(clean_database):
    email = "service_test@example.com"
    wrong_code = "false_code"

    AuthenticationService().generate_signup_verification_token(email)
    acceptance = AuthenticationService().validate_signup_verification_token(email, wrong_code)

    assert SignUpVerificationTokenRepository().count() == 1
    assert not acceptance


def test_service_create_code_unsuccesful(clean_database):
    email = "service_test@example.com"

    true_code = AuthenticationService().generate_signup_verification_token(email)
    acceptance = AuthenticationService().validate_signup_verification_token(email, true_code)

    assert SignUpVerificationTokenRepository().count() == 0
    assert acceptance
