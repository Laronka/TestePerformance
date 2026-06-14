from locust import HttpUser, task, between

class JuiceShopUser(HttpUser):
    host = "http://juice-shop:3000"
    wait_time = between(1, 3)

    @task
    def homepage(self):
        self.client.get("/")

    @task
    def busca(self):
        self.client.get("/rest/products/search?q=apple")
    
    @task
    def produto(self):
        self.client.get("/api/Products/1")

    @task
    def login(self):
        self.client.post("/rest/user/login", json={
        "email": "joaoiaronka622@gmail.com",
        "password": "Elo2026!"
    })