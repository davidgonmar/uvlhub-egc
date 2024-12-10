from locust import HttpUser, TaskSet, task, between
from core.environment.host import get_host_for_locust_testing
import random

class DatasetBehavior(TaskSet):
    def on_start(self):
        self.dataset()

    @task
    def dataset(self):
        response = self.client.post(
                '/explore',
                json={
                    "query": "wildlife",
                    **{}
                }
        )
        if response.status_code != 200:
            print(f"Search failed: {response.status_code}")


class DatasetUser(HttpUser):
    tasks = [DatasetBehavior]
    min_wait = 5000
    max_wait = 9000
    host = get_host_for_locust_testing()

class ExploreUser(HttpUser):
    host = "http://127.0.0.1:5000"
    wait_time = between(1, 5)

    def on_start(self):
        self.client.post("/login", data={
            "email": "user@example.com",
            "password": "test1234"
        })

    @task(3)
    def view_filters_with_default_parameters(self):
        url = "/explore?query=&publication_type=any&sorting=newest&start_date=&end_date=&min_uvl=&max_uvl=&min_size=&max_size=&size_unit=bytes"
        with self.client.get(url, catch_response=True) as response:
            if response.status_code == 200:
                print("Filters loaded successfully with default parameters.")
            else:
                print(f"Error loading filters with default parameters: {response.status_code}")
                response.failure(f"Got status code {response.status_code}")

    @task(2)
    def view_filters_with_custom_query(self):
        query = f"TestQuery{random.randint(1, 100)}"
        sorting = "oldest"
        publication_type = "datamanagementplan"
        url = f"/explore?query={query}&publication_type={publication_type}&sorting={sorting}&start_date=&end_date=&min_uvl=&max_uvl=&min_size=&max_size=&size_unit=bytes"
        with self.client.get(url, catch_response=True) as response:
            if response.status_code == 200:
                print(f"Filters loaded successfully with custom query: {query}")
            else:
                print(f"Error loading filters with custom query: {response.status_code}")
                response.failure(f"Got status code {response.status_code}")

    @task(2)
    def view_filters_with_date_range(self):
        start_date = "2024-01-01"
        end_date = "2024-12-31"
        url = f"/explore?query=&publication_type=any&sorting=newest&start_date={start_date}&end_date={end_date}&min_uvl=&max_uvl=&min_size=&max_size=&size_unit=bytes"
        with self.client.get(url, catch_response=True) as response:
            if response.status_code == 200:
                print(f"Filters loaded successfully with date range {start_date} to {end_date}.")
            else:
                print(f"Error loading filters with date range: {response.status_code}")
                response.failure(f"Got status code {response.status_code}")

    @task(2)
    def view_filters_with_uvl_range(self):
        min_uvl = random.randint(0, 2)
        max_uvl = random.randint(51, 100)
        url = f"/explore?query=&publication_type=any&sorting=newest&start_date=&end_date=&min_uvl={min_uvl}&max_uvl={max_uvl}&min_size=&max_size=&size_unit=bytes"
        with self.client.get(url, catch_response=True) as response:
            if response.status_code == 200:
                print(f"Filters loaded successfully with UVL range {min_uvl} to {max_uvl}.")
            else:
                print(f"Error loading filters with UVL range: {response.status_code}")
                response.failure(f"Got status code {response.status_code}")

    @task(1)
    def view_filters_with_size_range(self):
        min_size = random.randint(0, 1)
        max_size = random.randint(501, 1000)
        size_unit = "KB"
        url = f"/explore?query=&publication_type=any&sorting=newest&start_date=&end_date=&min_uvl=&max_uvl=&min_size={min_size}&max_size={max_size}&size_unit={size_unit}"
        with self.client.get(url, catch_response=True) as response:
            if response.status_code == 200:
                print(f"Filters loaded successfully with size range {min_size} KB to {max_size} KB.")
            else:
                print(f"Error loading filters with size range: {response.status_code}")
                response.failure(f"Got status code {response.status_code}")

    def on_stop(self):
        self.client.get("/logout")

