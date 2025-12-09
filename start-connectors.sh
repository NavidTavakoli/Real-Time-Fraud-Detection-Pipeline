#!/bin/bash

# Load environment variables
if [ -f .env ]; then
  export $(cat .env | xargs)
fi

echo "---"
echo "🔌 Initializing Debezium Connectors..."
echo "---"

# Wait for Connect service
until curl -s http://localhost:8083; do
  echo "⏳ Waiting for Kafka Connect..."
  sleep 5
done

# 1. MySQL Connector
echo "🚀 Submitting MySQL Connector..."
curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" \
  http://localhost:8083/connectors/ -d '{
  "name": "mysql-source",
  "config": {
    "connector.class": "io.debezium.connector.mysql.MySqlConnector",
    "tasks.max": "1",
    "database.hostname": "mysql",
    "database.port": "3306",
    "database.user": "root",
    "database.password": "'"${MYSQL_ROOT_PASS}"'",
    "database.server.id": "2",
    "topic.prefix": "mysqltopic",
    "schema.history.internal.kafka.bootstrap.servers": "kafka:9092",
    "schema.history.internal.kafka.topic": "schema-changes.mariadb",
    "database.include.list": "mariadb"
  }
}'

echo -e "\n--------------------------------\n"

# 2. Postgres Connector
echo "🚀 Submitting Postgres Connector..."
curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" \
  http://localhost:8083/connectors/ -d '{
  "name": "postgres-source",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "tasks.max": "1",
    "database.hostname": "postgres",
    "database.port": "5432",
    "database.user": "'"${POSTGRES_USER}"'",
    "database.password": "'"${POSTGRES_PASS}"'",
    "database.server.id": "1",
    "topic.prefix": "postgrestopic",
    "database.dbname": "'"${POSTGRES_DB}"'",
    "table.include.list": "public.customer",
    "plugin.name": "pgoutput",
    "database.history.kafka.bootstrap.servers": "kafka:9092",
    "database.history.kafka.topic": "schema-changes.postgres"
  }
}'

echo -e "\n✅ Done!"
