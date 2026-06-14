import random
from locust import HttpUser, task, between

produtos_id = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 13, 14, 15, 16, 17, 18, 19, 20,
    21, 22, 23, 24, 25, 26, 29, 30, 32, 33, 34, 35, 36, 37, 38,
    41, 42, 43, 45, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56
]


class JuiceShopUser(HttpUser):
    host = "http://juice-shop:3000"
    wait_time = between(1, 3)

    token = ""
    basket_id = None

    def on_start(self):
        self.produtos_no_carrinho = set()
        self.email = f"user_{id(self)}@juice.teste"

        self.client.post("/api/Users", json={
            "email": self.email,
            "password": "Elo2026",
            "passwordRepeat": "Elo2026",
            "securityQuestion": {
                "id": 1,
                "question": "Your eldest siblings middle name?"
            },
            "securityAnswer": "test"
        })

        resp = self.client.post("/rest/user/login", json={
            "email": self.email,
            "password": "Elo2026"
        })
        if resp.status_code == 200:
            dados = resp.json()["authentication"]
            self.token = dados["token"]
            self.basket_id = dados["bid"]

    @task(4)
    def homepage(self):
        self.client.get("/")

    @task(4)
    def busca(self):
        self.client.get("/rest/products/search?q=apple")

    @task(3)
    def produto(self):
        self.client.get("/api/Products/1")

    @task(2)
    def login(self):
        self.client.post("/rest/user/login", json={
            "email": self.email,
            "password": "Elo2026"
        })

    @task(1)
    def carrinho(self):
        if not self.token or not self.basket_id:
            return

        disponiveis = [i for i in produtos_id if i not in self.produtos_no_carrinho]
        if not disponiveis:
            return

        produto = random.choice(disponiveis)
        resp = self.client.post(
            "/api/BasketItems",
            json={
                "ProductId": produto,
                "BasketId": self.basket_id,
                "quantity": 1
            },
            headers={"Authorization": f"Bearer {self.token}"}
        )
        if resp.status_code in (200, 201):
            self.produtos_no_carrinho.add(produto)