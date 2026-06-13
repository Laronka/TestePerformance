from locust import HttpUser, task, between

class JuiceShopUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def homepage(self):
        self.client.get("/")