from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, LongType, ArrayType
import redis
import os

# --- Configuration ---
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = '6379'

# --- Schemas Definition ---
after_schema = StructType([
    StructField("age", LongType(), True),
    StructField("email", StringType(), True),
    StructField("id", LongType(), True),
    StructField("name", StringType(), True),
    StructField("purchase", LongType(), True),
    StructField("store", StringType(), True),
    StructField("timestamp", LongType(), True),
    StructField("clerk", StringType(), True)
])

# Standard Debezium Envelope Schema
source_schema = StructType([
    StructField("connector", StringType(), True),
    StructField("name", StringType(), True),
    StructField("ts_ms", LongType(), True),
    StructField("db", StringType(), True),
    StructField("table", StringType(), True)
])

payload_schema = StructType([
    StructField("after", after_schema, True),
    StructField("source", source_schema, True),
    StructField("op", StringType(), True)
])

complete_schema = StructType([
    StructField("payload", payload_schema, True)
])

# --- Spark Session Init ---
spark = SparkSession.builder \
    .appName("RealTime-Fraud-Detection") \
    .config("spark.redis.host", REDIS_HOST) \
    .config("spark.redis.port", REDIS_PORT) \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# --- Kafka Stream Readers ---
df_stream_postgres = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "postgrestopic.public.customer") \
    .load()

df_stream_mysql = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "mysqltopic.mariadb.customer") \
    .load()

# --- Data Parsing & Transformation ---
# Postgres Parsing
parsed_pg = df_stream_postgres.select(from_json(col("value").cast("string"), complete_schema).alias("data")) \
    .select("data.payload.after") \
    .selectExpr(
        "after.purchase AS pg_purchase",
        "after.clerk AS pg_clerk",
        "after.store AS pg_store"
    )

agg_pg = parsed_pg.groupBy("pg_clerk").agg(
    F.count("pg_purchase").alias("count"),
    F.sum("pg_purchase").alias("total_sales")
)

# MySQL Parsing
parsed_mysql = df_stream_mysql.select(from_json(col("value").cast("string"), complete_schema).alias("data")) \
    .select("data.payload.after") \
    .selectExpr(
        "after.purchase AS my_purchase",
        "after.clerk AS my_clerk",
        "after.store AS my_store"
    )

agg_mysql = parsed_mysql.groupBy("my_clerk").agg(
    F.count("my_purchase").alias("count"),
    F.sum("my_purchase").alias("total_sales")
)

# --- Redis Writers ---

def write_to_redis_mysql(df, epochId):
    """Writes MySQL aggregation results to Redis Hashes."""
    try:
        r = redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT), decode_responses=True)
        count = 0
        for row in df.collect():
            if row['my_clerk']:
                key = f"Mysql:{row['my_clerk']}"
                mapping = {
                    "Count": row['count'],
                    "Sum": row['total_sales']
                }
                r.hset(key, mapping=mapping)
                count += 1
        if count > 0:
            print(f"🟢 MySQL: Synced {count} clerks to Redis.")
    except Exception as e:
        print(f"❌ Error writing MySQL data to Redis: {e}")

def write_to_redis_postgres(df, epochId):
    """Writes Postgres aggregation results to Redis Hashes."""
    try:
        r = redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT), decode_responses=True)
        count = 0
        for row in df.collect():
            if row['pg_clerk']:
                key = f"Postgresql:{row['pg_clerk']}"
                mapping = {
                    "Count": row['count'],
                    "Sum": row['total_sales']
                }
                r.hset(key, mapping=mapping)
                count += 1
        if count > 0:
            print(f"🔵 Postgres: Synced {count} clerks to Redis.")
    except Exception as e:
        print(f"❌ Error writing Postgres data to Redis: {e}")

# --- Query Execution ---
query_mysql = agg_mysql.writeStream \
    .outputMode("update") \
    .foreachBatch(write_to_redis_mysql) \
    .trigger(processingTime='30 seconds') \
    .start()

query_pg = agg_pg.writeStream \
    .outputMode("update") \
    .foreachBatch(write_to_redis_postgres) \
    .trigger(processingTime='30 seconds') \
    .start()

query_mysql.awaitTermination()
query_pg.awaitTermination()
