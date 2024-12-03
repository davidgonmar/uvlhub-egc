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
    

# Although it is not a pure unit test, it can be classified under the "Partición Equivalente" technique.
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

    # Verificar que la respuesta tiene el estado correcto
    assert response.status_code == 200

    # Verify that the response has the correct status
    data = response.json
    assert len(data) == 1
    assert data[0]["title"] == "Dataset 1"

    # Verify that the repository was called correctly
    mock_filter.assert_called_once_with(
        query="tag1"
    ) 


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

    # Verificar que la respuesta tiene el estado correcto
    assert response.status_code == 200

    # Verify that the response has the correct status
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

    # Verificar que la respuesta tiene el estado correcto
    assert response.status_code == 200
    
    # Verify that the response has the correct status
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

    # Verificar que la respuesta tiene el estado correcto
    assert response.status_code == 200
    
    # Verify that the response has the correct status
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

    # Verificar que la respuesta tiene el estado correcto
    assert response.status_code == 200
    
    # Verify that the response has the correct status
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

    # Verificar que la respuesta tiene el estado correcto
    assert response.status_code == 200
    
    # Verify that the response has the correct status
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

    # Verificar que la respuesta tiene el estado correcto
    assert response.status_code == 200
    
    # Verify that the response has the correct status
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

    # Verificar que la respuesta tiene el estado correcto
    assert response.status_code == 200
    
    # Verify that the response has the correct status
    data = response.json

    # Assertions
    assert len(data) == 0
    mock_filter.assert_called_once_with(query="Description for dataset 5", **{})
  
    
