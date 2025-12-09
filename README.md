# 🕵️ Real-Time Retail Fraud Detection Pipeline

![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.9-blue?logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Apache Spark](https://img.shields.io/badge/Apache%20Spark-FDEE21?style=for-the-badge&logo=apachespark&logoColor=black)
![Apache Kafka](https://img.shields.io/badge/Apache%20Kafka-000?style=for-the-badge&logo=apachekafka)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)

A comprehensive **End-to-End Data Engineering Project** demonstrating a scalable, real-time Change Data Capture (CDC) pipeline.

This system simulates a high-velocity retail environment in Italy, capturing transactions from sharded operational databases (PostgreSQL & MySQL), streaming them via Kafka, processing aggregations using Apache Spark Structured Streaming, and serving real-time analytics via Redis.

## 🏗 System Architecture

![System Architecture Diagram](diagram.png)

## Data Flow Overview

1.  **Data Generation Layer**: A custom Python script (using Faker) generates realistic Italian retail transactions and inserts them directly into operational databases.
2.  **Operational Layer**: **PostgreSQL** and **MySQL** act as the source-of-truth databases, simulating a sharded environment.
3.  **Ingestion Layer (CDC)**: **Debezium** connectors monitor the database logs (WAL & Binlog) and stream row-level changes to **Kafka**.
4.  **Messaging Layer**: **Apache Kafka** decouples the ingestion from processing, buffering events in specific topics.
5.  **Processing Layer**: **Apache Spark Structured Streaming** consumes the streams, parses complex JSON payloads, and performs stateful aggregations (Sales per Clerk) in real-time.
6.  **Serving Layer**: **Redis** stores the aggregated metrics for low-latency access (Speed Layer).
7.  **Visualization Layer**: **Grafana** (connected to Redis) and **Kafka UI** provide monitoring dashboards.



## 📂 Project Structure

```
├── build/
│   ├── generator/
│   │   ├── Dockerfile       # Container setup for Python Data Generator
│   │   └── generateItems.py # Logic for generating Italian retail data
│   └── spark/
│       ├── Dockerfile       # Container setup for Spark
│       └── redisSink.py     # Spark Structured Streaming Job & Redis logic
├── docker-compose.yaml      # Orchestration for 11 microservices
├── start-connectors.sh      # Script to initialize Debezium connectors via API
├── .env.example             # Template for environment variables (Safe to share)
├── .env                     # Secrets & Credentials (Ignored by Git)
└── README.md                # Project Documentation
```



## 🛠 Tech Stack

| **Component**     | **Technology**    | **Description**                                              |
| ----------------- | ----------------- | ------------------------------------------------------------ |
| **Orchestration** | Docker Compose    | Manages the lifecycle of the entire stack (Network, Volumes). |
| **Data Gen**      | Python 3.9        | Simulates realistic transactions using the Faker library.    |
| **Databases**     | Postgres & MySQL  | Simulates a polyglot persistence layer (OLTP).               |
| **CDC**           | Debezium          | Captures database changes without polling.                   |
| **Broker**        | Kafka & Zookeeper | Handles high-throughput event streaming.                     |
| **Processing**    | Spark Streaming   | Performs stateful aggregations (Count/Sum).                  |
| **Storage**       | Redis             | In-memory NoSQL store for real-time dashboards.              |
| **Monitoring**    | Kafka UI          | Web UI for managing Kafka clusters and topics.               |

------

## 🚀 Getting Started

Follow these instructions to deploy the pipeline on your local machine or server.

### 1. Prerequisites

- Docker Engine & Docker Compose installed.
- **16GB RAM** recommended for optimal performance (minimum 8GB).

### 2. Configuration

Copy the example environment file to create your local secrets file. This file contains database passwords and configuration.

```
cp .env.example .env
```

> **Note:** You can modify `.env` to change passwords or ports if necessary.

### 3. Build & Launch

Build the custom Docker images and start the services in detached mode:

```
docker compose up --build -d
```

*Wait approximately 1-2 minutes for all containers (especially Kafka and Connect) to fully initialize.*

### 4. Activate Connectors

Once the containers are running, register the Debezium connectors to start the CDC process:

```
./start-connectors.sh
```

**Expected Output:** `HTTP/1.1 201 Created`

------

## 🧪 Verification & Monitoring

### 1. Verify Data in Redis

Check if the Spark job is successfully writing aggregated data to Redis:

```
docker exec -it redis redis-cli keys "*"
```

**Sample Output:**

Plaintext

```
1) "Mysql:Alessandro Del Piero"
2) "Postgresql:Giulia Bianchi"
3) "Postgresql:Francesco Totti"
...
```

### 2. Check Data Generator Logs

Ensure the Python script is inserting data correctly:

```
docker logs -f generator
```

### 3. Access Dashboards

- **Kafka UI:** `http://localhost:9090` - Monitor Topics & Consumers.
- **Grafana:** `http://localhost:3000` - Visualization (Login with credentials from `.env`).

------

## 🤝 Contributing

Contributions are welcome! Please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License.


