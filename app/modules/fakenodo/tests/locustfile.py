from locust import HttpUser, TaskSet, task
from core.environment.host import get_host_for_locust_testing


class FakenodoBehavior(TaskSet):
    def on_start(self):
        self.deposit_files_fakenodo()
        self.get_deposition_fakenodo()
        self.delete_deposition_fakenodo()

    @task
    def deposit_files_fakenodo(self):
        expected_message = "Successfully uploaded files to deposition 1"

        # Assuming depositionId is 1
        with self.client.post('/fakenodo/api/1/files', catch_response=True) as response:
            if response.status_code == 201 and expected_message in response.text:
                print("Successfully uploaded files to deposition 1")
            else:
                print(f"Error uploading files: {response.status_code}")
                response.failure(f"Got status code {response.status_code}")

    @task
    def get_deposition_fakenodo(self):
        expected_message = "Retrieved deposition with ID 1"

        # Assuming depositionId is 1
        with self.client.get('/fakenodo/api/1', catch_response=True) as response:
            if response.status_code == 200 and expected_message in response.text:
                print("Successfully retrieved deposition 1")
            else:
                print(f"Error getting deposition: {response.status_code}")
                response.failure(f"Got status code {response.status_code}")

    @task
    def delete_deposition_fakenodo(self):
        expected_message = "Successfully deleted deposition 1"

        # Assuming depositionId is 1
        with self.client.delete('/fakenodo/api/1', catch_response=True) as response:
            if response.status_code == 200 and expected_message in response.text:
                print("Successfully deleted deposition 1")
            else:
                print(f"Error deleting deposition: {response.status_code}")
                response.failure(f"Got status code {response.status_code}")


class DatasetUser(HttpUser):
    tasks = [FakenodoBehavior]
    min_wait = 5000
    max_wait = 9000
    host = get_host_for_locust_testing()
