import pytest

from app import db
from app.modules.conftest import login, logout
from app.modules.auth.models import User
from app.modules.profile.models import UserProfile


@pytest.fixture(scope="module")
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    for module testing (por example, new users)
    """
    with test_client.application.app_context():
        user_test = User(email='user@example.com', password='test1234', is_developer=True)
        user_test1 = User(email='user1@example.com', password='test1234')
        db.session.add(user_test)
        db.session.add(user_test1)
        db.session.commit()

        profile = UserProfile(user_id=user_test.id, name="Name", surname="Surname")
        profile1 = UserProfile(user_id=user_test1.id, name="Name", surname="Surname")
        db.session.add(profile)
        db.session.add(profile1)
        db.session.commit()

    yield test_client


def test_edit_profile_page_get(test_client):
    """
    Tests access to the profile editing page via a GET request.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.get("/profile/edit")
    assert response.status_code == 200, "The profile editing page could not be accessed."
    assert b"Edit profile" in response.data, "The expected content is not present on the page"

    logout(test_client)

def test_edit_post(test_client):
    """
    Tests access to the profile editing page via a GET request.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.post(
        "/profile/edit",
        data=dict(name="Foo",
                  surname="Example",
                  github="Cargarmar18",
                  orcid="0000-0000-0000-0000",
                  affiliation="Example affiliation"),
        follow_redirects=True,
    )
    assert response.status_code == 200

def test_edit_post_incorrect_github(test_client):
    """
    Tests that submitting an invalid GitHub username results in a validation error.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.post(
        "/profile/edit",
        data=dict(
            name="Foo",
            surname="Example",
            github="Cargarmar18",
            orcid="0000-0000-0000-0000",
            affiliation="Example affiliation"
        ),
        follow_redirects=True,
    )

    assert b"There was an error verifying your username, try again later please." in response.data, "Error message for invalid GitHub username not found."

    logout(test_client)

def test_edit_github_not_developer_user(test_client):
    """
    Tests that submitting an invalid GitHub username results in a validation error.
    """
    login_response = login(test_client, "user1@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.post(
        "/profile/edit",
        data=dict(
            name="Foo",
            surname="Example",
            github="Cargarmar18",
            orcid="0000-0000-0000-0000",
            affiliation="Example affiliation"
        ),
        follow_redirects=True,
    )

    assert b"Only developers can add their GitHub username." in response.data, "Error message for username being developer trying to add GitHub not found."

    logout(test_client)

def test_edit_incorrect_orcid(test_client):
    """
    Tests that submitting an invalid ORCID code results in a validation error.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.post(
        "/profile/edit",
        data=dict(
            name="Foo",
            surname="Example",
            github="foo@example.com",
            orcid="00-2134",
            affiliation="Example affiliation"
        ),
        follow_redirects=True,
    )

    assert b"ORCID must have 16 numbers separated by dashes" in response.data, "Error message for invalid ORCID not found."

    logout(test_client)
