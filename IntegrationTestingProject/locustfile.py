from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)  # Wait between 1 and 5 seconds between tasks

    @task
    def register(self):
        # Define the data for the POST request
        data = {
            "username": "testuser",
            "password": "password"
        }
        # Send a POST request to the /register endpoint
        self.client.post("/register", data=data)