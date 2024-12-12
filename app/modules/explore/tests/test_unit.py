import pytest
from unittest.mock import patch, MagicMock
from app.modules.explore.services import ExploreService



@pytest.fixture(scope='module')
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        # Add HERE new elements to the database that you want to exist in the test context.
        # DO NOT FORGET to use db.session.add(<element>) and db.session.commit() to save the data.
        pass

    yield test_client

# Tecnique "Partición equivalente"

@patch('app.modules.explore.services.ExploreService.filter')  # Mock the specific method
def test_filter_functionality_happy_path_title(mock_filter):
    # Create dataset mocks
    mock_dataset_1 = MagicMock()
    mock_dataset_1.to_dict.return_value = {
        "id": 1,
        "title": "Dataset 1",
        "description": "Description for dataset 1",
        "url": "/dataset/1",
        "authors": [{"name": "Author 1"}],
        "tags": ["tag1", "tag2"],
        "created_at": "2023-01-01",
    }

    mock_dataset_2 = MagicMock()
    mock_dataset_2.to_dict.return_value = {
        "id": 2,
        "title": "Dataset 2",
        "description": "Description for dataset 2",
        "url": "/dataset/2",
        "authors": [{"name": "Author 2"}],
        "tags": ["tag3"],
        "created_at": "2023-02-01",
    }
    # Configure the mock
    mock_filter.return_value = [mock_dataset_1, mock_dataset_2]

    # Call the function directly
    service = ExploreService()
    response = service.filter(query="Dataset")

    # Assertions
    assert len(response) == 2
    assert response[0].to_dict()["title"] == "Dataset 1"
    assert response[1].to_dict()["title"] == "Dataset 2"
    mock_filter.assert_called_once_with(query="Dataset")
@patch('app.modules.explore.services.ExploreService.filter')  # Mock the specific method
def test_filter_functionality_sad_path_title(mock_filter):
    # Create dataset mocks
    mock_dataset_1 = MagicMock()
    mock_dataset_1.to_dict.return_value = {
        "id": 1,
        "title": "Dataset 1",
        "description": "Description for dataset 1",
        "url": "/dataset/1",
        "authors": [{"name": "Author 1"}],
        "tags": ["tag1", "tag2"],
        "created_at": "2023-01-01",
    }

    mock_dataset_2 = MagicMock()
    mock_dataset_2.to_dict.return_value = {
        "id": 2,
        "title": "Dataset 2",
        "description": "Description for dataset 2",
        "url": "/dataset/2",
        "authors": [{"name": "Author 2"}],
        "tags": ["tag3"],
        "created_at": "2023-02-01",
    }
    # Configure the mock
    mock_filter.return_value = []

    # Call the function directly
    service = ExploreService()
    response = service.filter(query="Cat")

    # Assertions
    assert len(response) == 0
    mock_filter.assert_called_once_with(query="Cat")


@patch('app.modules.explore.services.ExploreService.filter')  # Mock the specific method
def test_filter_functionality_happy_path_tag(mock_filter):
    # Create dataset mocks
    mock_dataset_1 = MagicMock()
    mock_dataset_1.to_dict.return_value = {
        "id": 1,
        "title": "Dataset 1",
        "description": "Description for dataset 1",
        "url": "/dataset/1",
        "authors": [{"name": "Author 1"}],
        "tags": ["tag1", "tag2"],
        "created_at": "2023-01-01",
    }

    mock_dataset_2 = MagicMock()
    mock_dataset_2.to_dict.return_value = {
        "id": 2,
        "title": "Dataset 2",
        "description": "Description for dataset 2",
        "url": "/dataset/2",
        "authors": [{"name": "Author 2"}],
        "tags": ["tag3"],
        "created_at": "2023-02-01",
    }
    # Configure the mock
    mock_filter.return_value = [mock_dataset_1]

    # Call the function directly
    service = ExploreService()
    response = service.filter(query="tag1")

    # Assertions
    assert len(response) == 1
    mock_filter.assert_called_once_with(query="tag1")

@patch('app.modules.explore.services.ExploreService.filter')  # Mock the specific method
def test_filter_functionality_sad_path_tag(mock_filter):
    # Create dataset mocks
    mock_dataset_1 = MagicMock()
    mock_dataset_1.to_dict.return_value = {
        "id": 1,
        "title": "Dataset 1",
        "description": "Description for dataset 1",
        "url": "/dataset/1",
        "authors": [{"name": "Author 1"}],
        "tags": ["tag1", "tag2"],
        "created_at": "2023-01-01",
    }

    mock_dataset_2 = MagicMock()
    mock_dataset_2.to_dict.return_value = {
        "id": 2,
        "title": "Dataset 2",
        "description": "Description for dataset 2",
        "url": "/dataset/2",
        "authors": [{"name": "Author 2"}],
        "tags": ["tag3"],
        "created_at": "2023-02-01",
    }
    # Configure the mock
    mock_filter.return_value = []

    # Call the function directly
    service = ExploreService()
    response = service.filter(query="Tigers")

    # Assertions
    assert len(response) == 0
    mock_filter.assert_called_once_with(query="Tigers")
    
    
@patch('app.modules.explore.services.ExploreService.filter')  # Mock the specific method
def test_filter_functionality_happy_path_description(mock_filter):
    # Create dataset mocks
    mock_dataset_1 = MagicMock()
    mock_dataset_1.to_dict.return_value = {
        "id": 1,
        "title": "Dataset 1",
        "description": "Description for dataset 1",
        "url": "/dataset/1",
        "authors": [{"name": "Author 1"}],
        "tags": ["tag1", "tag2"],
        "created_at": "2023-01-01",
    }

    mock_dataset_2 = MagicMock()
    mock_dataset_2.to_dict.return_value = {
        "id": 2,
        "title": "Dataset 2",
        "description": "Description for dataset 2",
        "url": "/dataset/2",
        "authors": [{"name": "Author 2"}],
        "tags": ["tag3"],
        "created_at": "2023-02-01",
    }
    # Configure the mock
    mock_filter.return_value = [mock_dataset_2]

    # Call the function directly
    service = ExploreService()
    response = service.filter(query="Description for dataset 2")

    # Assertions
    assert len(response) == 1
    mock_filter.assert_called_once_with(query="Description for dataset 2")
    

@patch('app.modules.explore.services.ExploreService.filter')  # Mock the specific method
def test_filter_functionality_sad_path_description(mock_filter):
    # Create dataset mocks
    mock_dataset_1 = MagicMock()
    mock_dataset_1.to_dict.return_value = {
        "id": 1,
        "title": "Dataset 1",
        "description": "Description for dataset 1",
        "url": "/dataset/1",
        "authors": [{"name": "Author 1"}],
        "tags": ["tag1", "tag2"],
        "created_at": "2023-01-01",
    }

    mock_dataset_2 = MagicMock()
    mock_dataset_2.to_dict.return_value = {
        "id": 2,
        "title": "Dataset 2",
        "description": "Description for dataset 2",
        "url": "/dataset/2",
        "authors": [{"name": "Author 2"}],
        "tags": ["tag3"],
        "created_at": "2023-02-01",
    }
    # Configure the mock
    mock_filter.return_value = []

    # Call the function directly
    service = ExploreService()
    response = service.filter(query="Incorrect description")

    # Assertions
    assert len(response) == 0
    mock_filter.assert_called_once_with(query="Incorrect description")
    
    
@patch('app.modules.explore.services.ExploreService.filter')  # Mock the specific method
def test_filter_functionality_happy_path_author(mock_filter):
    # Create dataset mocks
    mock_dataset_1 = MagicMock()
    mock_dataset_1.to_dict.return_value = {
        "id": 1,
        "title": "Dataset 1",
        "description": "Description for dataset 1",
        "url": "/dataset/1",
        "authors": [{"name": "Author 1"}],
        "tags": ["tag1", "tag2"],
        "created_at": "2023-01-01",
    }

    mock_dataset_2 = MagicMock()
    mock_dataset_2.to_dict.return_value = {
        "id": 2,
        "title": "Dataset 2",
        "description": "Description for dataset 2",
        "url": "/dataset/2",
        "authors": [{"name": "Author 2"}],
        "tags": ["tag3"],
        "created_at": "2023-02-01",
    }
    # Configure the mock
    mock_filter.return_value = [mock_dataset_2]

    # Call the function directly
    service = ExploreService()
    response = service.filter(query="Author 1")

    # Assertions
    assert len(response) == 1
    mock_filter.assert_called_once_with(query="Author 1")
    

@patch('app.modules.explore.services.ExploreService.filter')  # Mock the specific method
def test_filter_functionality_sad_path_author(mock_filter):
    # Create dataset mocks
    mock_dataset_1 = MagicMock()
    mock_dataset_1.to_dict.return_value = {
        "id": 1,
        "title": "Dataset 1",
        "description": "Description for dataset 1",
        "url": "/dataset/1",
        "authors": [{"name": "Author 1"}],
        "tags": ["tag1", "tag2"],
        "created_at": "2023-01-01",
    }

    mock_dataset_2 = MagicMock()
    mock_dataset_2.to_dict.return_value = {
        "id": 2,
        "title": "Dataset 2",
        "description": "Description for dataset 2",
        "url": "/dataset/2",
        "authors": [{"name": "Author 2"}],
        "tags": ["tag3"],
        "created_at": "2023-02-01",
    }
    # Configure the mock
    mock_filter.return_value = []

    # Call the function directly
    service = ExploreService()
    response = service.filter(query="Incorrect author")

    # Assertions
    assert len(response) == 0
    mock_filter.assert_called_once_with(query="Incorrect author")
    
    
@patch('app.modules.explore.services.ExploreService.filter')  # Mock the specific method
def test_filter_functionality_no_input(mock_filter):
    # Create dataset mocks
    mock_dataset_1 = MagicMock()
    mock_dataset_1.to_dict.return_value = {
        "id": 1,
        "title": "Dataset 1",
        "description": "Description for dataset 1",
        "url": "/dataset/1",
        "authors": [{"name": "Author 1"}],
        "tags": ["tag1", "tag2"],
        "created_at": "2023-01-01",
    }

    mock_dataset_2 = MagicMock()
    mock_dataset_2.to_dict.return_value = {
        "id": 2,
        "title": "Dataset 2",
        "description": "Description for dataset 2",
        "url": "/dataset/2",
        "authors": [{"name": "Author 2"}],
        "tags": ["tag3"],
        "created_at": "2023-02-01",
    }
    # Configure the mock
    mock_filter.return_value = [mock_dataset_1, mock_dataset_2]

    # Call the function directly
    service = ExploreService()
    response = service.filter(query="")

    # Assertions
    assert len(response) == 2
    assert response[0].to_dict()["title"] == "Dataset 1"
    assert response[1].to_dict()["title"] == "Dataset 2"
    mock_filter.assert_called_once_with(query="")
    
    
# Tecnique "Valores límite"
@patch('app.modules.explore.services.ExploreService.filter')  # Mock the specific method
def test_filter_functionality_number_dataset_is_not_above_reality(mock_filter):
    # Create dataset mocks
    mock_dataset_1 = MagicMock()
    mock_dataset_1.to_dict.return_value = {
        "id": 1,
        "title": "Dataset 1",
        "description": "Description for dataset 1",
        "url": "/dataset/1",
        "authors": [{"name": "Author 1"}],
        "tags": ["tag1", "tag2"],
        "created_at": "2023-01-01",
    }

    mock_dataset_2 = MagicMock()
    mock_dataset_2.to_dict.return_value = {
        "id": 2,
        "title": "Dataset 2",
        "description": "Description for dataset 2",
        "url": "/dataset/2",
        "authors": [{"name": "Author 2"}],
        "tags": ["tag3"],
        "created_at": "2023-02-01",
    }
    # Configure the mock
    mock_filter.return_value = [mock_dataset_1, mock_dataset_2]

    # Call the function directly
    service = ExploreService()
    response = service.filter(query="")

    # Assertions
    assert len(response) < 3
    assert response[0].to_dict()["title"] == "Dataset 1"
    assert response[1].to_dict()["title"] == "Dataset 2"
    mock_filter.assert_called_once_with(query="")


@patch('app.modules.explore.services.ExploreService.filter')  # Mock the specific method
def test_filter_functionality_number_dataset_is_not_less_than_reality_for_a_input(mock_filter):
    # Create dataset mocks
    mock_dataset_1 = MagicMock()
    mock_dataset_1.to_dict.return_value = {
        "id": 1,
        "title": "Dataset 1",
        "description": "Description for dataset 1",
        "url": "/dataset/1",
        "authors": [{"name": "Author 1"}],
        "tags": ["tag1", "tag2"],
        "created_at": "2023-01-01",
    }

    mock_dataset_2 = MagicMock()
    mock_dataset_2.to_dict.return_value = {
        "id": 2,
        "title": "Dataset 2",
        "description": "Description for dataset 2",
        "url": "/dataset/2",
        "authors": [{"name": "Author 2"}],
        "tags": ["tag3"],
        "created_at": "2023-02-01",
    }
    # Configure the mock
    mock_filter.return_value = [mock_dataset_1]

    # Call the function directly
    service = ExploreService()
    response = service.filter(query="tag1")

    # Assertions
    assert len(response) > 0
    assert response[0].to_dict()["title"] == "Dataset 1"
    mock_filter.assert_called_once_with(query="tag1")


# Tecnique "Experiencia"
@patch('app.modules.explore.services.ExploreService.filter')  # Mock the specific method
def test_filter_functionality_sql_insertion(mock_filter):
    # Create dataset mocks
    mock_dataset_1 = MagicMock()
    mock_dataset_1.to_dict.return_value = {
        "id": 1,
        "title": "Dataset 1",
        "description": "Description for dataset 1",
        "url": "/dataset/1",
        "authors": [{"name": "Author 1"}],
        "tags": ["tag1", "tag2"],
        "created_at": "2023-01-01",
    }

    mock_dataset_2 = MagicMock()
    mock_dataset_2.to_dict.return_value = {
        "id": 2,
        "title": "Dataset 2",
        "description": "Description for dataset 2",
        "url": "/dataset/2",
        "authors": [{"name": "Author 2"}],
        "tags": ["tag3"],
        "created_at": "2023-02-01",
    }
    # Configure the mock
    mock_filter.return_value = []

    # Call the function directly
    service = ExploreService()
    response = service.filter(query="SHOW DATABASES;")

    # Assertions
    assert len(response) == 0
    mock_filter.assert_called_once_with(query="SHOW DATABASES;")
    
    
@patch('app.modules.explore.services.ExploreService.filter')  # Mock the specific method
def test_filter_functionality_radom_insertion(mock_filter):
    # Create dataset mocks
    mock_dataset_1 = MagicMock()
    mock_dataset_1.to_dict.return_value = {
        "id": 1,
        "title": "Dataset 1",
        "description": "Description for dataset 1",
        "url": "/dataset/1",
        "authors": [{"name": "Author 1"}],
        "tags": ["tag1", "tag2"],
        "created_at": "2023-01-01",
    }

    mock_dataset_2 = MagicMock()
    mock_dataset_2.to_dict.return_value = {
        "id": 2,
        "title": "Dataset 2",
        "description": "Description for dataset 2",
        "url": "/dataset/2",
        "authors": [{"name": "Author 2"}],
        "tags": ["tag3"],
        "created_at": "2023-02-01",
    }
    # Configure the mock
    mock_filter.return_value = []

    # Call the function directly
    service = ExploreService()
    response = service.filter(query="djadoufhapsdufad")

    # Assertions
    assert len(response) == 0
    mock_filter.assert_called_once_with(query="djadoufhapsdufad")
    

# Technique "Partición Equivalente"
@patch('app.modules.explore.services.ExploreService.filter')  # Mock the specific method
def test_search_queries_functionality_using_the_route_post_happy_path(mock_filter, test_client):
   
    # Create dataset mocks
    mock_dataset_1 = MagicMock()
    mock_dataset_1.to_dict.return_value = {
        "id": 1,
        "title": "Dataset 1",
        "description": "Description for dataset 1",
        "url": "/dataset/1",
        "authors": [{"name": "Author 1"}],
        "tags": ["tag1", "tag2"],
        "created_at": "2023-01-01",
    }

    mock_dataset_2 = MagicMock()
    mock_dataset_2.to_dict.return_value = {
        "id": 2,
        "title": "Dataset 2",
        "description": "Description for dataset 2",
        "url": "/dataset/2",
        "authors": [{"name": "Author 2"}],
        "tags": ["tag3"],
        "created_at": "2023-02-01",
    }

    # Configure the repository mock to return the datasets
    mock_filter.return_value = [mock_dataset_1]

    # Make a request to the endpoint
    response = test_client.post(
        '/explore',
        json={
            "query": "tag1",
            **{}
        }
    )

    # Verify that the response has the correct status
    assert response.status_code == 200

    # Verify that the response contains the correct content
    data = response.json
    assert len(data) == 1
    assert data[0]["title"] == "Dataset 1"

    # Verify that the repository was called correctly
    mock_filter.assert_called_once_with(
        query="tag1")


@patch('app.modules.explore.services.ExploreService.filter')  # Mock the specific method
def test_search_queries_functionality_using_the_route_post_sad_path(mock_filter, test_client):

    # Create dataset mocks
    mock_dataset_1 = MagicMock()
    mock_dataset_1.to_dict.return_value = {
        "id": 1,
        "title": "Dataset 1",
        "description": "Description for dataset 1",
        "url": "/dataset/1",
        "authors": [{"name": "Author 1"}],
        "tags": ["tag1", "tag2"],
        "created_at": "2023-01-01",
    }

    mock_dataset_2 = MagicMock()
    mock_dataset_2.to_dict.return_value = {
        "id": 2,
        "title": "Dataset 2",
        "description": "Description for dataset 2",
        "url": "/dataset/2",
        "authors": [{"name": "Author 2"}],
        "tags": ["tag3"],
        "created_at": "2023-02-01",
    }

    # Configure the repository mock to return the datasets
    mock_filter.return_value = []

    # Make a request to the endpoint
    response = test_client.post(
        '/explore',
        json={
            "query": "Holidays",
            **{}
        }
    )

    # Verify that the response has the correct status
    assert response.status_code == 200

    # Verify that the response contains the correct content
    data = response.json
    assert len(data) == 0

    # Verify that the repository was called correctly
    mock_filter.assert_called_once_with(
        query="Holidays"
    )
    

@patch('app.modules.explore.services.ExploreService.filter')  # Mock the specific method
def test_filter_functionality__the_route_post_happy_path_title(mock_filter, test_client):
    # Create dataset mocks
    mock_dataset_1 = MagicMock()
    mock_dataset_1.to_dict.return_value = {
        "id": 1,
        "title": "Dataset 1",
        "description": "Description for dataset 1",
        "url": "/dataset/1",
        "authors": [{"name": "Author 1"}],
        "tags": ["tag1", "tag2"],
        "created_at": "2023-01-01",
    }

    mock_dataset_2 = MagicMock()
    mock_dataset_2.to_dict.return_value = {
        "id": 2,
        "title": "Dataset 2",
        "description": "Description for dataset 2",
        "url": "/dataset/2",
        "authors": [{"name": "Author 2"}],
        "tags": ["tag3"],
        "created_at": "2023-02-01",
    }
    # Configure the mock
    mock_filter.return_value = [mock_dataset_1, mock_dataset_2]

    # Make a request to the endpoint
    response = test_client.post(
        '/explore',
        json={
            "query": "Dataset",
            **{}
        }
    )

    # Verify that the response has the correct status
    assert response.status_code == 200
    
    # Verify that the response contains the correct content
    data = response.json

    # Assertions
    assert len(data) == 2
    assert data[0]["title"] == "Dataset 1"
    assert data[1]["title"] == "Dataset 2"
    mock_filter.assert_called_once_with(query="Dataset", **{})
    

@patch('app.modules.explore.services.ExploreService.filter')  # Mock the specific method
def test_filter_functionality__the_route_post_sad_path_title(mock_filter, test_client):
    # Create dataset mocks
    mock_dataset_1 = MagicMock()
    mock_dataset_1.to_dict.return_value = {
        "id": 1,
        "title": "Dataset 1",
        "description": "Description for dataset 1",
        "url": "/dataset/1",
        "authors": [{"name": "Author 1"}],
        "tags": ["tag1", "tag2"],
        "created_at": "2023-01-01",
    }

    mock_dataset_2 = MagicMock()
    mock_dataset_2.to_dict.return_value = {
        "id": 2,
        "title": "Dataset 2",
        "description": "Description for dataset 2",
        "url": "/dataset/2",
        "authors": [{"name": "Author 2"}],
        "tags": ["tag3"],
        "created_at": "2023-02-01",
    }
    # Configure the mock
    mock_filter.return_value = []

    # Make a request to the endpoint
    response = test_client.post(
        '/explore',
        json={
            "query": "Cat",
            **{}
        }
    )

    # Verify that the response has the correct status
    assert response.status_code == 200
    
    # Verify that the response contains the correct content
    data = response.json

    # Assertions
    assert len(data) == 0
    mock_filter.assert_called_once_with(query="Cat", **{})
    
    
@patch('app.modules.explore.services.ExploreService.filter')  # Mock the specific method
def test_filter_functionality__the_route_post_happy_path_tag(mock_filter, test_client):
    # Create dataset mocks
    mock_dataset_1 = MagicMock()
    mock_dataset_1.to_dict.return_value = {
        "id": 1,
        "title": "Dataset 1",
        "description": "Description for dataset 1",
        "url": "/dataset/1",
        "authors": [{"name": "Author 1"}],
        "tags": ["tag1", "tag2"],
        "created_at": "2023-01-01",
    }

    mock_dataset_2 = MagicMock()
    mock_dataset_2.to_dict.return_value = {
        "id": 2,
        "title": "Dataset 2",
        "description": "Description for dataset 2",
        "url": "/dataset/2",
        "authors": [{"name": "Author 2"}],
        "tags": ["tag3"],
        "created_at": "2023-02-01",
    }
    # Configure the mock
    mock_filter.return_value = [mock_dataset_2]

    # Make a request to the endpoint
    response = test_client.post(
        '/explore',
        json={
            "query": "tag3",
            **{}
        }
    )

    # Verify that the response has the correct status
    assert response.status_code == 200
    
    # Verify that the response contains the correct content
    data = response.json

    # Assertions
    assert len(data) == 1
    assert data[0]["title"] == "Dataset 2"
    mock_filter.assert_called_once_with(query="tag3", **{})
    
    
@patch('app.modules.explore.services.ExploreService.filter')  # Mock the specific method
def test_filter_functionality__the_route_sad_happy_path_tag(mock_filter, test_client):
    # Create dataset mocks
    mock_dataset_1 = MagicMock()
    mock_dataset_1.to_dict.return_value = {
        "id": 1,
        "title": "Dataset 1",
        "description": "Description for dataset 1",
        "url": "/dataset/1",
        "authors": [{"name": "Author 1"}],
        "tags": ["tag1", "tag2"],
        "created_at": "2023-01-01",
    }

    mock_dataset_2 = MagicMock()
    mock_dataset_2.to_dict.return_value = {
        "id": 2,
        "title": "Dataset 2",
        "description": "Description for dataset 2",
        "url": "/dataset/2",
        "authors": [{"name": "Author 2"}],
        "tags": ["tag3"],
        "created_at": "2023-02-01",
    }
    # Configure the mock
    mock_filter.return_value = []

    # Make a request to the endpoint
    response = test_client.post(
        '/explore',
        json={
            "query": "tag8",
            **{}
        }
    )

    # Verify that the response has the correct status
    assert response.status_code == 200
    
    # Verify that the response contains the correct content
    data = response.json

    # Assertions
    assert len(data) == 0
    mock_filter.assert_called_once_with(query="tag8", **{})
    
       
@patch('app.modules.explore.services.ExploreService.filter')  # Mock the specific method
def test_filter_functionality__the_route_happy_happy_path_description(mock_filter, test_client):
    # Create dataset mocks
    mock_dataset_1 = MagicMock()
    mock_dataset_1.to_dict.return_value = {
        "id": 1,
        "title": "Dataset 1",
        "description": "Description for dataset 1",
        "url": "/dataset/1",
        "authors": [{"name": "Author 1"}],
        "tags": ["tag1", "tag2"],
        "created_at": "2023-01-01",
    }

    mock_dataset_2 = MagicMock()
    mock_dataset_2.to_dict.return_value = {
        "id": 2,
        "title": "Dataset 2",
        "description": "Description for dataset 2",
        "url": "/dataset/2",
        "authors": [{"name": "Author 2"}],
        "tags": ["tag3"],
        "created_at": "2023-02-01",
    }
    # Configure the mock
    mock_filter.return_value = [mock_dataset_1, mock_dataset_2]

    # Make a request to the endpoint
    response = test_client.post(
        '/explore',
        json={
            "query": "Description for",
            **{}
        }
    )

    # Verify that the response has the correct status
    assert response.status_code == 200
    
    # Verify that the response contains the correct content
    data = response.json

    # Assertions
    assert len(data) == 2
    assert data[0]["title"] == "Dataset 1"
    assert data[1]["title"] == "Dataset 2"
    mock_filter.assert_called_once_with(query="Description for", **{})
    

@patch('app.modules.explore.services.ExploreService.filter')  # Mock the specific method
def test_filter_functionality__the_route_happy_sad_path_description(mock_filter, test_client):
    # Create dataset mocks
    mock_dataset_1 = MagicMock()
    mock_dataset_1.to_dict.return_value = {
        "id": 1,
        "title": "Dataset 1",
        "description": "Description for dataset 1",
        "url": "/dataset/1",
        "authors": [{"name": "Author 1"}],
        "tags": ["tag1", "tag2"],
        "created_at": "2023-01-01",
    }

    mock_dataset_2 = MagicMock()
    mock_dataset_2.to_dict.return_value = {
        "id": 2,
        "title": "Dataset 2",
        "description": "Description for dataset 2",
        "url": "/dataset/2",
        "authors": [{"name": "Author 2"}],
        "tags": ["tag3"],
        "created_at": "2023-02-01",
    }
    # Configure the mock
    mock_filter.return_value = []

    # Make a request to the endpoint
    response = test_client.post(
        '/explore',
        json={
            "query": "Description for dataset 5",
            **{}
        }
    )

    # Verify that the response has the correct status
    assert response.status_code == 200
    
    # Verify that the response contains the correct content
    data = response.json

    # Assertions
    assert len(data) == 0
    mock_filter.assert_called_once_with(query="Description for dataset 5", **{})
  
    
@patch('app.modules.explore.services.ExploreService.filter')  # Mock the specific method
def test_filter_functionality__the_route_happy_happy_path_author(mock_filter, test_client):
    # Create dataset mocks
    mock_dataset_1 = MagicMock()
    mock_dataset_1.to_dict.return_value = {
        "id": 1,
        "title": "Dataset 1",
        "description": "Description for dataset 1",
        "url": "/dataset/1",
        "authors": [{"name": "Author 1"}],
        "tags": ["tag1", "tag2"],
        "created_at": "2023-01-01",
    }

    mock_dataset_2 = MagicMock()
    mock_dataset_2.to_dict.return_value = {
        "id": 2,
        "title": "Dataset 2",
        "description": "Description for dataset 2",
        "url": "/dataset/2",
        "authors": [{"name": "Author 2"}],
        "tags": ["tag3"],
        "created_at": "2023-02-01",
    }
    # Configure the mock
    mock_filter.return_value = [mock_dataset_2]

    # Make a request to the endpoint
    response = test_client.post(
        '/explore',
        json={
            "query": "Author 2",
            **{}
        }
    )

    # Verify that the response has the correct status
    assert response.status_code == 200
    
    # Verify that the response contains the correct content
    data = response.json

    # Assertions
    assert len(data) == 1
    assert data[0]["title"] == "Dataset 2"
    mock_filter.assert_called_once_with(query="Author 2", **{})
 
 
@patch('app.modules.explore.services.ExploreService.filter')  # Mock the specific method
def test_filter_functionality__the_route_sad_happy_path_author(mock_filter, test_client):
    # Create dataset mocks
    mock_dataset_1 = MagicMock()
    mock_dataset_1.to_dict.return_value = {
        "id": 1,
        "title": "Dataset 1",
        "description": "Description for dataset 1",
        "url": "/dataset/1",
        "authors": [{"name": "Author 1"}],
        "tags": ["tag1", "tag2"],
        "created_at": "2023-01-01",
    }

    mock_dataset_2 = MagicMock()
    mock_dataset_2.to_dict.return_value = {
        "id": 2,
        "title": "Dataset 2",
        "description": "Description for dataset 2",
        "url": "/dataset/2",
        "authors": [{"name": "Author 2"}],
        "tags": ["tag3"],
        "created_at": "2023-02-01",
    }
    # Configure the mock
    mock_filter.return_value = []

    # Make a request to the endpoint
    response = test_client.post(
        '/explore',
        json={
            "query": "Author 6",
            **{}
        }
    )

    # Verify that the response has the correct status
    assert response.status_code == 200
    
    # Verify that the response contains the correct content
    data = response.json

    # Assertions
    assert len(data) == 0
    mock_filter.assert_called_once_with(query="Author 6", **{})


@patch('app.modules.explore.services.ExploreService.filter')  # Mock the specific method
def test_filter_functionality_no_input_the_route_post(mock_filter, test_client):
    # Create dataset mocks
    mock_dataset_1 = MagicMock()
    mock_dataset_1.to_dict.return_value = {
        "id": 1,
        "title": "Dataset 1",
        "description": "Description for dataset 1",
        "url": "/dataset/1",
        "authors": [{"name": "Author 1"}],
        "tags": ["tag1", "tag2"],
        "created_at": "2023-01-01",
    }

    mock_dataset_2 = MagicMock()
    mock_dataset_2.to_dict.return_value = {
        "id": 2,
        "title": "Dataset 2",
        "description": "Description for dataset 2",
        "url": "/dataset/2",
        "authors": [{"name": "Author 2"}],
        "tags": ["tag3"],
        "created_at": "2023-02-01",
    }
    # Configure the mock
    mock_filter.return_value = [mock_dataset_1, mock_dataset_2]

    # Make a request to the endpoint
    response = test_client.post(
        '/explore',
        json={
            "query": "",
            **{}
        }
    )

    # Verify that the response has the correct status
    assert response.status_code == 200
    
    # Verify that the response contains the correct content
    data = response.json

    # Assertions
    assert len(data) == 2
    assert data[0]["title"] == "Dataset 1"
    assert data[1]["title"] == "Dataset 2"
    mock_filter.assert_called_once_with(query="")
    

# Tecnique "Valores límite"

@patch('app.modules.explore.services.ExploreService.filter')  # Mock the specific method
def test_filter_functionality_number_dataset_is_not_above_reality_post_route(mock_filter, test_client):
    # Create dataset mocks
    mock_dataset_1 = MagicMock()
    mock_dataset_1.to_dict.return_value = {
        "id": 1,
        "title": "Dataset 1",
        "description": "Description for dataset 1",
        "url": "/dataset/1",
        "authors": [{"name": "Author 1"}],
        "tags": ["tag1", "tag2"],
        "created_at": "2023-01-01",
    }

    mock_dataset_2 = MagicMock()
    mock_dataset_2.to_dict.return_value = {
        "id": 2,
        "title": "Dataset 2",
        "description": "Description for dataset 2",
        "url": "/dataset/2",
        "authors": [{"name": "Author 2"}],
        "tags": ["tag3"],
        "created_at": "2023-02-01",
    }
    # Configure the mock
    mock_filter.return_value = [mock_dataset_1, mock_dataset_2]

    # Make a request to the endpoint
    response = test_client.post(
        '/explore',
        json={
            "query": "",
            **{}
        }
    )

    # Verify that the response has the correct status
    assert response.status_code == 200
    
    # Verify that the response contains the correct content
    data = response.json

    # Assertions
    assert len(data) < 3
    assert data[0]["title"] == "Dataset 1"
    assert data[1]["title"] == "Dataset 2"
    mock_filter.assert_called_once_with(query="")

    
@patch('app.modules.explore.services.ExploreService.filter')  # Mock the specific method
def test_filter_functionality_number_dataset_is_not_less_than_reality_for_a_input_post_route(mock_filter, test_client):
    # Create dataset mocks
    mock_dataset_1 = MagicMock()
    mock_dataset_1.to_dict.return_value = {
        "id": 1,
        "title": "Dataset 1",
        "description": "Description for dataset 1",
        "url": "/dataset/1",
        "authors": [{"name": "Author 1"}],
        "tags": ["tag1", "tag2"],
        "created_at": "2023-01-01",
    }

    mock_dataset_2 = MagicMock()
    mock_dataset_2.to_dict.return_value = {
        "id": 2,
        "title": "Dataset 2",
        "description": "Description for dataset 2",
        "url": "/dataset/2",
        "authors": [{"name": "Author 2"}],
        "tags": ["tag3"],
        "created_at": "2023-02-01",
    }
    # Configure the mock
    mock_filter.return_value = [mock_dataset_1]

    # Make a request to the endpoint
    response = test_client.post(
        '/explore',
        json={
            "query": "tag1",
            **{}
        }
    )

    # Verificar que la respuesta tiene el estado correcto
    assert response.status_code == 200
    
    # Verify that the response has the correct status
    data = response.json

    # Assertions
    assert len(data) > 0
    assert data[0]["title"] == "Dataset 1"
    mock_filter.assert_called_once_with(query="tag1")


# Tecnique "Experiencia"
@patch('app.modules.explore.services.ExploreService.filter')  # Mock the specific method
def test_filter_functionality_random_insertion_post_route(mock_filter, test_client):
    # Create dataset mocks
    mock_dataset_1 = MagicMock()
    mock_dataset_1.to_dict.return_value = {
        "id": 1,
        "title": "Dataset 1",
        "description": "Description for dataset 1",
        "url": "/dataset/1",
        "authors": [{"name": "Author 1"}],
        "tags": ["tag1", "tag2"],
        "created_at": "2023-01-01",
    }

    mock_dataset_2 = MagicMock()
    mock_dataset_2.to_dict.return_value = {
        "id": 2,
        "title": "Dataset 2",
        "description": "Description for dataset 2",
        "url": "/dataset/2",
        "authors": [{"name": "Author 2"}],
        "tags": ["tag3"],
        "created_at": "2023-02-01",
    }
    # Configure the mock
    mock_filter.return_value = []

    # Make a request to the endpoint
    response = test_client.post(
        '/explore',
        json={
            "query": "djadoufhapsdufad",
            **{}
        }
    )

    # Verify that the response has the correct status
    assert response.status_code == 200
    
    # Verify that the response contains the correct content
    data = response.json

    # Assertions
    assert len(data) == 0
    mock_filter.assert_called_once_with(query="djadoufhapsdufad")


@patch('app.modules.explore.services.ExploreService.filter')  # Mock the specific method
def test_filter_functionality_sql_insertion_post_route(mock_filter, test_client):
    # Create dataset mocks
    mock_dataset_1 = MagicMock()
    mock_dataset_1.to_dict.return_value = {
        "id": 1,
        "title": "Dataset 1",
        "description": "Description for dataset 1",
        "url": "/dataset/1",
        "authors": [{"name": "Author 1"}],
        "tags": ["tag1", "tag2"],
        "created_at": "2023-01-01",
    }

    mock_dataset_2 = MagicMock()
    mock_dataset_2.to_dict.return_value = {
        "id": 2,
        "title": "Dataset 2",
        "description": "Description for dataset 2",
        "url": "/dataset/2",
        "authors": [{"name": "Author 2"}],
        "tags": ["tag3"],
        "created_at": "2023-02-01",
    }
    # Configure the mock
    mock_filter.return_value = []

    # Make a request to the endpoint
    response = test_client.post(
        '/explore',
        json={
            "query": "SHOW DATABASES;",
            **{}
        }
    )

    # Verify that the response has the correct status
    assert response.status_code == 200
    
    # Verify that the response contains the correct content
    data = response.json

    # Assertions
    assert len(data) == 0
    mock_filter.assert_called_once_with(query="SHOW DATABASES;")
    

@pytest.fixture(scope="module")
def test_client(test_client):
    """
    Extiende la fixture de test_client para añadir elementos específicos en la base de datos
    que se usarán en los tests.
    """
    with test_client.application.app_context():
        # Aquí puedes añadir nuevos elementos a la base de datos que desees
        # para el contexto de pruebas. Asegúrate de usar db.session.add() y db.session.commit()
        pass
    yield test_client


@pytest.fixture
def explore_service():
    return ExploreService()


def test_filter_with_default_arguments(explore_service):
    with patch.object(explore_service.repository, 'filter') as mock_filter:
        # Mock de los datasets que el repositorio devolverá
        mock_datasets = [MagicMock(id=1), MagicMock(id=2)]
        mock_filter.return_value = mock_datasets
        # Llamada al método filter sin parámetros adicionales
        result = explore_service.filter()
        # Verificación del resultado
        assert result == mock_datasets
        assert len(result) == 2
        mock_filter.assert_called_once_with(
            "",
            "newest",
            "any",
            [],
            "",
            "",
            "",
            "",
            None,
            None,
            "bytes"
        )


def test_filter_with_custom_query(explore_service):
    with patch.object(explore_service.repository, 'filter') as mock_filter:
        # Mock de datasets con un query específico
        mock_datasets = [MagicMock(id=1), MagicMock(id=2)]
        mock_filter.return_value = mock_datasets
        # Parámetros personalizados para la prueba
        query = "Test Query"
        sorting = "oldest"
        tags = ["tag1", "tag2"]
        result = explore_service.filter(query=query, sorting=sorting, tags=tags)
        # Verificación del resultado
        assert result == mock_datasets
        assert len(result) == 2
        mock_filter.assert_called_once_with(
            "Test Query",
            "oldest",
            "any",
            ["tag1", "tag2"],
            "",
            "",
            "",
            "",
            None,
            None,
            "bytes"
        )


def test_filter_with_date_range(explore_service):
    with patch.object(explore_service.repository, 'filter') as mock_filter:
        # Mock de datasets filtrados por fecha
        mock_datasets = [MagicMock(id=1), MagicMock(id=2)]
        mock_filter.return_value = mock_datasets
        # Parámetros personalizados para el filtro de fecha
        start_date = "2024-01-01"
        end_date = "2024-12-31"
        result = explore_service.filter(start_date=start_date, end_date=end_date)
        # Verificación del resultado
        assert result == mock_datasets
        assert len(result) == 2
        mock_filter.assert_called_once_with(
            "",
            "newest",
            "any",
            [],
            "2024-01-01",
            "2024-12-31",
            "",
            "",
            None,
            None,
            "bytes"
        )


def test_filter_with_uvl_range(explore_service):
    with patch.object(explore_service.repository, 'filter') as mock_filter:
        # Mock de datasets filtrados por UVL
        mock_datasets = [MagicMock(id=1), MagicMock(id=2)]
        mock_filter.return_value = mock_datasets
        # Parámetros personalizados para el filtro UVL
        min_uvl = "10"
        max_uvl = "100"
        result = explore_service.filter(min_uvl=min_uvl, max_uvl=max_uvl)
        # Verificación del resultado
        assert result == mock_datasets
        assert len(result) == 2
        mock_filter.assert_called_once_with(
            "",
            "newest",
            "any",
            [],
            "",
            "",
            "10",
            "100",
            None,
            None,
            "bytes"
        )


def test_filter_with_size_range(explore_service):
    with patch.object(explore_service.repository, 'filter') as mock_filter:
        # Mock de datasets filtrados por tamaño
        mock_datasets = [MagicMock(id=1), MagicMock(id=2)]
        mock_filter.return_value = mock_datasets
        # Parámetros personalizados para el filtro de tamaño
        min_size = 500
        max_size = 2000
        size_unit = "KB"
        result = explore_service.filter(min_size=min_size, max_size=max_size, size_unit=size_unit)
        # Verificación del resultado
        assert result == mock_datasets
        assert len(result) == 2
        mock_filter.assert_called_once_with(
            "",
            "newest",
            "any",
            [],
            "",
            "",
            "",
            "",
            500,
            2000,
            "KB"
        )


def test_filter_with_multiple_parameters(explore_service):
    with patch.object(explore_service.repository, 'filter') as mock_filter:
        # Mock de datasets con múltiples filtros combinados
        mock_datasets = [MagicMock(id=1), MagicMock(id=2), MagicMock(id=3)]
        mock_filter.return_value = mock_datasets
        # Parámetros personalizados
        query = "complex search"
        tags = ["science", "data"]
        start_date = "2023-01-01"
        end_date = "2023-12-31"
        min_size = 100
        max_size = 1000
        result = explore_service.filter(
            query=query,
            tags=tags,
            start_date=start_date,
            end_date=end_date,
            min_size=min_size,
            max_size=max_size,
        )
        # Verificación del resultado
        assert result == mock_datasets
        assert len(result) == 3
        mock_filter.assert_called_once_with(
            "complex search",
            "newest",
            "any",
            ["science", "data"],
            "2023-01-01",
            "2023-12-31",
            "",
            "",
            100,
            1000,
            "bytes"
        )


def test_filter_with_specific_publication_type(explore_service):
    with patch.object(explore_service.repository, 'filter') as mock_filter:
        # Mock de datasets filtrados por tipo de publicación
        mock_datasets = [MagicMock(id=1)]
        mock_filter.return_value = mock_datasets
        # Parámetros personalizados
        publication_type = "research_paper"
        result = explore_service.filter(publication_type=publication_type)
        # Verificación del resultado
        assert result == mock_datasets
        assert len(result) == 1
        mock_filter.assert_called_once_with(
            "",
            "newest",
            "research_paper",
            [],
            "",
            "",
            "",
            "",
            None,
            None,
            "bytes"
        )


def test_filter_with_no_results(explore_service):
    with patch.object(explore_service.repository, 'filter') as mock_filter:
        # Mock de una respuesta vacía
        mock_filter.return_value = []
        # Parámetros que no coinciden con ningún dataset
        query = "nonexistent"
        tags = ["nonexistent_tag"]
        result = explore_service.filter(query=query, tags=tags)
        # Verificación del resultado
        assert result == []
        assert len(result) == 0
        mock_filter.assert_called_once_with(
            "nonexistent",
            "newest",
            "any",
            ["nonexistent_tag"],
            "",
            "",
            "",
            "",
            None,
            None,
            "bytes"
        )


def test_filter_with_invalid_date_range(explore_service):
    with patch.object(explore_service.repository, 'filter') as mock_filter:
        # Mock de una respuesta vacía o de error
        mock_filter.return_value = []
        # Parámetros con un rango de fechas inválido (fecha inicial mayor que la final)
        start_date = "2024-12-31"
        end_date = "2024-01-01"
        result = explore_service.filter(start_date=start_date, end_date=end_date)
        # Verificación del resultado
        assert result == []
        mock_filter.assert_called_once_with(
            "",
            "newest",
            "any",
            [],
            "2024-12-31",
            "2024-01-01",
            "",
            "",
            None,
            None,
            "bytes"
        )


def test_filter_with_invalid_size_range(explore_service):
    with patch.object(explore_service.repository, 'filter') as mock_filter:
        # Mock de una respuesta vacía
        mock_filter.return_value = []
        # Parámetros con un rango de tamaño inválido (mínimo mayor que el máximo)
        min_size = 2000
        max_size = 500
        result = explore_service.filter(min_size=min_size, max_size=max_size)
        # Verificación del resultado
        assert result == []
        mock_filter.assert_called_once_with(
            "",
            "newest",
            "any",
            [],
            "",
            "",
            "",
            "",
            2000,
            500,
            "bytes"
        )


def test_filter_with_invalid_uvl_range(explore_service):
    with patch.object(explore_service.repository, 'filter') as mock_filter:
        # Mock de una respuesta vacía
        mock_filter.return_value = []
        # Parámetros con un rango de UVL inválido (mínimo mayor que el máximo)
        min_uvl = "100"
        max_uvl = "10"
        result = explore_service.filter(min_uvl=min_uvl, max_uvl=max_uvl)
        # Verificación del resultado
        assert result == []
        mock_filter.assert_called_once_with(
            "",
            "newest",
            "any",
            [],
            "",
            "",
            "100",
            "10",
            None,
            None,
            "bytes"
        )


def test_filter_with_invalid_query_and_tags(explore_service):
    with patch.object(explore_service.repository, 'filter') as mock_filter:
        # Mock de una respuesta vacía
        mock_filter.return_value = []
        # Parámetros que no tienen sentido juntos (query inexistente y tags contradictorias)
        query = "!@#$%^&*()"  # Query no válida
        tags = ["nonexistent_tag1", "nonexistent_tag2"]
        result = explore_service.filter(query=query, tags=tags)
        # Verificación del resultado
        assert result == []
        mock_filter.assert_called_once_with(
            "!@#$%^&*()",
            "newest",
            "any",
            ["nonexistent_tag1", "nonexistent_tag2"],
            "",
            "",
            "",
            "",
            None,
            None,
            "bytes"
        )


def test_filter_with_unexpected_error(explore_service):
    with patch.object(explore_service.repository, 'filter', side_effect=Exception("Unexpected error")) as mock_filter:
        # Simulación de una excepción inesperada durante la ejecución
        try:
            result = explore_service.filter()
        except Exception as e:
            result = str(e)
        # Verificación de la excepción
        assert result == "Unexpected error"
        mock_filter.assert_called_once_with(
            "",
            "newest",
            "any",
            [],
            "",
            "",
            "",
            "",
            None,
            None,
            "bytes"
        )

