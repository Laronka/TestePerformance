from locust import HttpUser, task, between

@task
def homepage(self):
    self.client.get("/")