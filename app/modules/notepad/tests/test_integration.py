import pytest

from app import db
from app.modules.conftest import login, logout
from app.modules.auth.models import User
from app.modules.profile.models import UserProfile
from flask_login import current_user

@pytest.fixture(scope="module")
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        user_test = User(email='user@example.com', password='test1234')
        db.session.add(user_test)
        db.session.commit()

        profile = UserProfile(user_id=user_test.id, name="Name", surname="Surname")
        db.session.add(profile)
        db.session.commit()

    yield test_client


def test_get_notepad(test_client):
    """
    Test retrieving a specific notepad via GET request.
    """
    # Log in the test user
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    # Create a notepad
    response = test_client.post('/notepad/create', data={
        'title': 'Notepad2',
        'body': 'This is the body of notepad2.'
    }, follow_redirects=True)
    assert response.status_code == 200

    # Get the notepad ID from the database
    with test_client.application.app_context():
        from app.modules.notepad.models import Notepad
        notepad = Notepad.query.filter_by(title='Notepad2', user_id=current_user.id).first()
        assert notepad is not None, "Notepad was not found in the database."

    # Access the notepad detail page
    response = test_client.get(f'/notepad/{notepad.id}')
    assert response.status_code == 200, "The notepad detail page could not be accessed."
    assert b'Notepad2' in response.data, "The notepad title is not present on the page."

    logout(test_client)

def test_edit_notepad(test_client):
    """
    Test editing a notepad via POST request.
    """
    # Log in the test user
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    # Create a notepad
    response = test_client.post('/notepad/create', data={
        'title': 'Notepad3',
        'body': 'This is the body of notepad3.'
    }, follow_redirects=True)
    assert response.status_code == 200

    # Get the notepad ID from the database
    with test_client.application.app_context():
        from app.modules.notepad.models import Notepad
        notepad = Notepad.query.filter_by(title='Notepad3', user_id=current_user.id).first()
        assert notepad is not None, "Notepad was not found in the database."

    # Edit the notepad
    response = test_client.post(f'/notepad/edit/{notepad.id}', data={
        'title': 'Notepad3 Edited',
        'body': 'This is the edited body of notepad3.'
    }, follow_redirects=True)
    assert response.status_code == 200, "The notepad could not be edited."

    # Check that the notepad was updated
    with test_client.application.app_context():
        notepad = Notepad.query.get(notepad.id)
        assert notepad.title == 'Notepad3 Edited', "The notepad title was not updated."
        assert notepad.body == 'This is the edited body of notepad3.', "The notepad body was not updated."

    logout(test_client)

def test_delete_notepad(test_client):
    """
    Test deleting a notepad via POST request.
    """
    # Log in the test user
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    # Create a notepad
    response = test_client.post('/notepad/create', data={
        'title': 'Notepad4',
        'body': 'This is the body of notepad4.'
    }, follow_redirects=True)
    assert response.status_code == 200

    # Get the notepad ID from the database
    with test_client.application.app_context():
        from app.modules.notepad.models import Notepad
        notepad = Notepad.query.filter_by(title='Notepad4', user_id=current_user.id).first()
        assert notepad is not None, "Notepad was not found in the database."

    # Delete the notepad
    response = test_client.post(f'/notepad/delete/{notepad.id}', follow_redirects=True)
    assert response.status_code == 200, "The notepad could not be deleted."

    # Check that the notepad was deleted
    with test_client.application.app_context():
        notepad = Notepad.query.get(notepad.id)
        assert notepad is None, "The notepad was not deleted."

    logout(test_client)