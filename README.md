# Testes de Performance — OWASP Juice Shop

Projeto de testes de performance para a disciplina de Testes e Qualidade de Software, utilizando Locust e OWASP Juice Shop containerizados com Docker.

---

## Estrutura do projeto

```
TestePerformance/
├── docker-compose.yml           # Sobe o Juice Shop
├── docker-compose.locust.yml    # Sobe o Locust (runner de testes)
├── locustfile.py                # Cenários de teste
├── results/                     # CSVs gerados pelos testes
│   ├── load_10u_stats.csv
│   ├── load_25u_stats.csv
│   ├── load_50u_stats.csv
│   ├── load_100u_stats.csv
│   └── load_200u_stats.csv
└── README.md
```

---

## Pré-requisitos

- Docker Desktop instalado e em execução
- Terminal (PowerShell ou CMD no Windows)

---

## Como executar

### 1. Clonar o repositório

```bash
git clone https://github.com/Laronka/TestePerformance
cd TestePerformance
```

### 2. Subir o Juice Shop

```bash
docker-compose up -d
```

Aguarde alguns segundos e acesse `http://localhost:3000` no navegador para confirmar que a loja está no ar.

### 3. Rodar os testes

Execute um de cada vez, aguardando o anterior terminar:

**10 usuários — carga baixa:**
```bash
docker-compose -f docker-compose.locust.yml run --rm locust -f locustfile.py --headless -u 10 -r 2 -t 60s --csv results/load_10u
```

**25 usuários — carga baixa-média:**
```bash
docker-compose -f docker-compose.locust.yml run --rm locust -f locustfile.py --headless -u 25 -r 3 -t 60s --csv results/load_25u
```

**50 usuários — carga média:**
```bash
docker-compose -f docker-compose.locust.yml run --rm locust -f locustfile.py --headless -u 50 -r 5 -t 60s --csv results/load_50u
```

**100 usuários — carga alta:**
```bash
docker-compose -f docker-compose.locust.yml run --rm locust -f locustfile.py --headless -u 100 -r 10 -t 60s --csv results/load_100u
```

**200 usuários — colapso:**
```bash
docker-compose -f docker-compose.locust.yml run --rm locust -f locustfile.py --headless -u 200 -r 20 -t 60s --csv results/load_200u
```

### 4. Verificar os resultados

Após cada teste, os arquivos CSV são salvos em `results/`:

| Arquivo | Conteúdo |
|---------|----------|
| `load_Xu_stats.csv` | Métricas por endpoint (p90, p95, throughput) |
| `load_Xu_stats_history.csv` | Evolução das métricas ao longo do tempo |
| `load_Xu_failures.csv` | Erros ocorridos durante o teste |
| `load_Xu_exceptions.csv` | Exceções do Locust |

### 5. Encerrar o Juice Shop

```bash
docker-compose down
```

---

## Cenários de teste

| # | Cenário | Método | Endpoint | Peso |
|---|---------|--------|----------|------|
| 1 | Página inicial | GET | `/` | 4 |
| 2 | Busca de produtos | GET | `/rest/products/search?q=apple` | 4 |
| 3 | Detalhe de produto | GET | `/api/Products/1` | 3 |
| 4 | Login de usuário | POST | `/rest/user/login` | 2 |
| 5 | Adicionar ao carrinho | POST | `/api/BasketItems` | 1 |

Os pesos definem a probabilidade de cada cenário ser sorteado pelo Locust. Cenários com peso maior são executados com mais frequência, simulando o comportamento real de usuários de e-commerce — mais navegação e busca, menos compras.

---

## Níveis de carga

| Nível | Usuários | Spawn rate | Duração |
|-------|----------|------------|---------|
| Baixo | 10 | 2/s | 60s |
| Baixo-médio | 25 | 3/s | 60s |
| Médio | 50 | 5/s | 60s |
| Alto | 100 | 10/s | 60s |
| Colapso | 200 | 20/s | 60s |

---

## Observações

- O Juice Shop recria o banco de dados toda vez que o container é reiniciado. O `locustfile.py` cria automaticamente uma conta de teste no `on_start` antes de iniciar os cenários, portanto não é necessário criar usuários manualmente.
- Os testes rodam em containers Docker isolados com recursos limitados (Juice Shop: 3 cores / 4GB RAM, Locust: 2 cores / 2GB RAM) para evitar que os dois processos compitam pelos mesmos recursos da máquina. Essa separação foi recomendada pelo professor para garantir que o Locust e o Juice Shop não disputem os mesmos recursos, o que distorceria os resultados.
- O container do Locust é removido automaticamente após cada teste (`--rm`).

