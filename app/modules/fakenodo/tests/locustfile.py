from locust import HttpUser, TaskSet, task, between


class FakenodoTaskSet(TaskSet):

    @task(1)
    def test_connection(self):
        self.client.get("/fakenodo/api/test_connection")

    @task(2)
    def create_deposition(self):
        data = {"dataset_id": 1}  
        self.client.post("/fakenodo/api/depositions", json=data)

    @task(2)
    def upload_file(self):
        data = {
            "dataset_id": 1,
            "feature_model_id": 1
        }
        deposition_id = 1
        self.client.post(f"/fakenodo/api/{deposition_id}/files", data=data)

    @task(1)
    def publish_deposition(self):
        deposition_id = 1
        self.client.put(f"/fakenodo/api/{deposition_id}/publish")

    @task(1)
    def get_deposition(self):
        deposition_id = 1
        self.client.get(f"/fakenodo/api/{deposition_id}")

    @task(1)
    def get_doi(self):
        deposition_id = 1
        self.client.get(f"/fakenodo/api/{deposition_id}/doi")

    @task(1)
    def get_all_depositions(self):
        self.client.get("/fakenodo/api/depositions")

    @task(1)
    def delete_deposition(self):
        deposition_id = 1
        self.client.delete(f"/fakenodo/api/{deposition_id}")


class FakenodoUser(HttpUser):
    host = "http://127.0.0.1:5000"
    tasks = [FakenodoTaskSet]
    wait_time = between(1, 5)
