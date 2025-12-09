# 🕵️ Real-Time Fraud Detection Pipeline

A comprehensive Data Engineering project demonstrating a real-time CDC (Change Data Capture) pipeline using **Kafka**, **Spark Streaming**, **Debezium**, and **Redis**.

## 🏗 Architecture

1.  **Data Generation**: Python script simulates Italian retail transactions.
2.  **Databases**: PostgreSQL and MySQL store raw transactions.
3.  **CDC (Debezium)**: Captures DB changes and streams them to Kafka.
4.  **Processing (Spark)**: Aggregates sales per clerk in real-time.
5.  **Storage (Redis)**: Stores live analytics.
6.  **Visualization**: Grafana (Optional) or Redis CLI.

## 🚀 How to Run

### 1. Prerequisites
* Docker & Docker Compose

### 2. Setup Configuration
Create a `.env` file in the root directory (do not commit this file):

```ini
POSTGRES_USER=postgres
POSTGRES_PASS=123456
POSTGRES_DB=postgres

MYSQL_ROOT_PASS=debezium
MYSQL_USER=mysqluser
MYSQL_PASS=mysqlpw
MYSQL_DB=mariadb

GRAFANA_USER=admin
GRAFANA_PASS=admin

KAFKA_HOST=kafka
REDIS_HOST=redis
```

### 3. Launch the Pipeline
```bash
docker compose up --build -d
```

### 4. Activate Connectors
Once containers are running (wait ~1 min), run:
```bash
./start-connectors.sh
```

### 5. Verify
Check real-time data in Redis:
```bash
docker exec -it redis redis-cli keys "*"
```
