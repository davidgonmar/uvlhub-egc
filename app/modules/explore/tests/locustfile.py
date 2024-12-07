from locust import HttpUser, TaskSet, task
from core.environment.host import get_host_for_locust_testing


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
        