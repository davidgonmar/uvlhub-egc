from locust import HttpUser, task, between
import random

class NotepadUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        # Login at the start of each simulated user session
        self.client.post("/login", data={
            "email": "user@example.com",
            "password": "test1234"
        })

    @task(3)
    def view_notepads(self):
        with self.client.get("/notepad", catch_response=True) as response:
            if response.status_code == 200:
                print("Notepad list loaded successfully.")
            else:
                print(f"Error loading notepad list: {response.status_code}")
                response.failure(f"Got status code {response.status_code}")

    @task(2)
    def create_notepad(self):
        new_notepad = {
            "title": f"Notepad created by Locust {random.randint(1, 1000)}",
            "body": "This is a test notepad created during load testing."
        }
        with self.client.post("/notepad/create", data=new_notepad, catch_response=True) as response:
            if response.status_code == 200:
                print("Notepad created successfully.")
            else:
                print(f"Error creating notepad: {response.status_code}")
                response.failure(f"Got status code {response.status_code}")

    @task(1)
    def view_specific_notepad(self):
        # Assuming notepad IDs are between 1 and 1000. Adjust as needed.
        notepad_id = random.randint(1, 1000)
        with self.client.get(f"/notepad/{notepad_id}", catch_response=True) as response:
            if response.status_code == 200:
                print(f"Notepad {notepad_id} loaded successfully.")
            elif response.status_code == 404:
                print(f"Notepad {notepad_id} not found.")
            else:
                print(f"Error loading notepad {notepad_id}: {response.status_code}")
                response.failure(f"Got status code {response.status_code}")

    def on_stop(self):
        # Logout at the end of each simulated user session
        self.client.get("/logout")
