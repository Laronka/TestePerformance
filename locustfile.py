from locust import HttpUser, task, between

class JuiceShopUser(HttpUser):
    host = "http://juice-shop:3000"
    wait_time = between(1, 3)

    token = ""
    basket_id = None

    def on_start(self):
        
        self.client.post("/api/Users", json={
            "email": "joaoiaronka622@gmail.com",
            "password": "Elo2026",
            "passwordRepeat": "Elo2026",
            "securityQuestion": {
                "id": 1,
                "question": "Your eldest siblings middle name?"
            },
            "securityAnswer": "test"
        })

        resp = self.client.post("/rest/user/login", json={
            "email": "joaoiaronka622@gmail.com",
            "password": "Elo2026"
        })
        if resp.status_code == 200:
            dados = resp.json()["authentication"]
            self.token = dados["token"]
            self.basket_id = dados["bid"]

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
        "password": "Elo2026"
    })
    @task
    def carrinho(self):
         self.client.post("/api/BasketItems", json={
        "ProductId": 1,
        "BasketId": 1,
        "quantity": 1
    })