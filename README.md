cat <<EOF > README.md
# 🕵️ Real-Time Retail Fraud Detection Pipeline

![License](https://img.shields.io/badge/license-MIT-blue)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Apache Spark](https://img.shields.io/badge/Apache%20Spark-FDEE21?style=for-the-badge&logo=apachespark&logoColor=black)
![Apache Kafka](https://img.shields.io/badge/Apache%20Kafka-000?style=for-the-badge&logo=apachekafka)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)

A comprehensive **End-to-End Data Engineering Project** designed to detect anomalies and aggregate sales data in real-time. This project simulates a retail environment in Italy, capturing transactions from multiple databases, processing them via Spark Streaming, and visualizing the results.

---

## 🏗 System Architecture

The following diagram illustrates the data flow from generation to visualization.
*(This diagram renders automatically on GitHub)*.

![diagram](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)

---

## 🛠 Tech Stack & Features

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Orchestration** | **Docker Compose** | Manages the lifecycle of 10+ microservices. |
| **Data Gen** | **Python (Faker)** | Simulates realistic transactions with Italian metadata. |
| **Databases** | **Postgres & MySQL** | Simulates sharded operational databases (OLTP). |
| **Ingestion** | **Debezium** | Performs CDC (Change Data Capture) to stream DB changes. |
| **Broker** | **Kafka & Zookeeper** | Decouples the source databases from the processing layer. |
| **Processing** | **Spark Streaming** | Reads Kafka streams, parses JSON, and performs aggregations. |
| **State Store** | **Redis** | Stores the real-time aggregated metrics for low-latency access. |
| **Monitoring** | **Kafka UI & Grafana** | Provides visibility into topics and final metrics. |

---

## 📂 Project Structure

\`\`\`bash
├── build/
│   ├── generator/       # Python script & Dockerfile for data generation
│   └── spark/           # Spark job (Redis Sink) & Dockerfile
├── docker-compose.yaml  # Main infrastructure definition
├── start-connectors.sh  # Script to initialize Debezium connectors
├── .env                 # Secrets (Not committed to Git)
└── README.md            # Documentation
\`\`\`

---

## 🚀 Getting Started

Follow these steps to deploy the pipeline on your local machine or server.

### 1. Prerequisites
* Docker Engine & Docker Compose installed.
* 4GB+ RAM available.

### 2. Setup Environment Variables
Create a \`.env\` file in the root directory. **Do not commit this file.**

\`\`\`ini
# Database Credentials
POSTGRES_USER=postgres
POSTGRES_PASS=123456
POSTGRES_DB=postgres

MYSQL_ROOT_PASS=debezium
MYSQL_USER=mysqluser
MYSQL_PASS=mysqlpw
MYSQL_DB=mariadb

# Visualization
GRAFANA_USER=admin
GRAFANA_PASS=admin

# Infrastructure
KAFKA_HOST=kafka
REDIS_HOST=redis
\`\`\`

### 3. Build & Launch
This command builds the custom images for Spark and the Generator, then starts all services.

\`\`\`bash
docker compose up --build -d
\`\`\`

### 4. Activate Connectors
Wait about 60 seconds for Kafka Connect to start, then register the Debezium connectors:

\`\`\`bash
./start-connectors.sh
\`\`\`
*You should see a \`201 Created\` response.*

---

## 🧪 Verification

### Check Data Flow
You can inspect the real-time data being written to Redis:

\`\`\`bash
docker exec -it redis redis-cli keys "*"
\`\`\`

**Expected Output:**
\`\`\`text
1) "Mysql:Alessandro Del Piero"
2) "Postgresql:Giulia Bianchi"
3) "Postgresql:Fabio Capello"
...
\`\`\`

### Monitoring
* **Kafka UI**: Access at \`http://localhost:9090\` to view topics and messages.
* **Grafana**: Access at \`http://localhost:3000\` (Login with credentials from .env).

---

## 🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License
[MIT](https://choosealicense.com/licenses/mit/)
EOF
