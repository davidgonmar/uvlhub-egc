import pytest
from unittest.mock import patch, MagicMock
from app.modules.notepad.services import NotepadService
from app.modules.notepad.models import Notepad
from app.modules.auth.models import User

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
def notepad_service():
    return NotepadService()

def test_get_all_by_user(notepad_service):
    with patch.object(notepad_service.repository, 'get_all_by_user') as mock_get_all:
        mock_notepads = [MagicMock(id=1), MagicMock(id=2)]
        mock_get_all.return_value = mock_notepads

        user_id = 1
        result = notepad_service.get_all_by_user(user_id)

        assert result == mock_notepads
        assert len(result) == 2
        mock_get_all.assert_called_once_with(user_id)

def test_create(notepad_service):
    with patch.object(notepad_service.repository, 'create') as mock_create:
        mock_notepad = MagicMock(id=1)
        mock_create.return_value = mock_notepad

        title = 'Test Notepad'
        body = 'Test Body'
        user_id = 1

        result = notepad_service.create(title=title, body=body, user_id=user_id)

        assert result == mock_notepad
        assert result.id == 1
        mock_create.assert_called_once_with(title=title, body=body, user_id=user_id)

def test_update(notepad_service):
    with patch.object(notepad_service.repository, 'update') as mock_update:
        mock_notepad = MagicMock(id=1)
        mock_update.return_value = mock_notepad

        notepad_id = 1
        title = 'Updated Notepad'
        body = 'Updated Body'

        result = notepad_service.update(notepad_id, title=title, body=body)

        assert result == mock_notepad
        mock_update.assert_called_once_with(notepad_id, title=title, body=body)


def test_delete(notepad_service):
    with patch.object(notepad_service.repository, 'delete') as mock_delete:
        mock_delete.return_value = True

        notepad_id = 1
        result = notepad_service.delete(notepad_id)

        assert result is True
        mock_delete.assert_called_once_with(notepad_id)

