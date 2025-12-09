from datetime import datetime
import random
import time
import psycopg2
import pymysql
import os

# --- Database Connection Configuration ---
# Fetching credentials from environment variables for security

postgres_conn_params = {
    'database': os.getenv('POSTGRES_DB', 'postgres'),
    'user': os.getenv('POSTGRES_USER', 'postgres'),
    'password': os.getenv('POSTGRES_PASS', '123456'),
    'host': 'postgres',
    'port': 5432
}

mariadb_conn_params = {
    'database': os.getenv('MYSQL_DB', 'mariadb'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASS', 'debezium'),
    'host': 'mysql',
    'port': 3306
}

# --- Data Generation Lists (Italian Context) ---
italian_first_names = [
    "Mario", "Luigi", "Giovanni", "Giuseppe", "Antonio", "Francesco", "Alessandro", "Leonardo", "Lorenzo", "Mattia",
    "Sofia", "Giulia", "Aurora", "Alice", "Ginevra", "Emma", "Giorgia", "Maria", "Anna", "Chiara"
]

italian_last_names = [
    "Rossi", "Russo", "Ferrari", "Esposito", "Bianchi", "Romano", "Colombo", "Ricci",
    "Marino", "Greco", "Bruno", "Gallo", "Conti", "De Luca", "Mancini", "Costa", "Giordano", "Rizzo"
]

italian_clerks = [
    "Fabio Capello", "Roberto Baggio", "Andrea Pirlo", "Gianluigi Buffon", "Alessandro Del Piero",
    "Francesco Totti", "Paolo Maldini", "Gennaro Gattuso", "Carlo Ancelotti", "Antonio Conte"
]

# --- Helper Functions ---

def generate_italian_identity():
    """Generates a random Italian name and email."""
    first = random.choice(italian_first_names)
    last = random.choice(italian_last_names)
    full_name = f"{first} {last}"
    email_domain = random.choice(['libero.it', 'virgilio.it', 'email.it', 'gmail.com'])
    email = f"{first.lower()}.{last.lower()}{random.randint(1,99)}@{email_domain}"
    return full_name, email

def generate_random_data_postgres():
    """Generates a data payload for Postgres."""
    name, email = generate_italian_identity()
    return {
        'name': name,
        'age': random.randint(18, 75),
        'email': email,
        'purchase': random.randint(1_000, 100_000_000),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'store': random.choice(['S1', 'S3', 'S5', 'S7']),
        'clerk': random.choice(italian_clerks)
    }

def generate_random_data_mysql():
    """Generates a data payload for MySQL."""
    name, email = generate_italian_identity()
    return {
        'name': name,
        'age': random.randint(18, 75),
        'email': email,
        'purchase': random.randint(1_000, 100_000_000),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'store': random.choice(['S2', 'S4', 'S6']),
        'clerk': random.choice(italian_clerks)
    }

def create_tables_if_not_exist():
    """Initializes tables if they don't exist (Handling clean restarts)."""
    # Postgres
    try:
        with psycopg2.connect(**postgres_conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS customer (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255),
                        age INT,
                        email VARCHAR(255),
                        purchase INT,
                        store VARCHAR(50),
                        timestamp VARCHAR(50),
                        clerk VARCHAR(50)
                    );
                """)
                conn.commit()
        print("✅ Postgres table ensured.")
    except Exception as e:
        print(f"⚠️ Postgres init skipped (will retry): {e}")

    # MySQL
    try:
        with pymysql.connect(**mariadb_conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute("CREATE DATABASE IF NOT EXISTS mariadb;")
                cur.execute("USE mariadb;")
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS customer (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255),
                        age INT,
                        email VARCHAR(255),
                        purchase INT,
                        store VARCHAR(50),
                        timestamp VARCHAR(50),
                        clerk VARCHAR(50)
                    );
                """)
                conn.commit()
        print("✅ MySQL table ensured.")
    except Exception as e:
        print(f"⚠️ MySQL init skipped (will retry): {e}")

def insert_postgres(data):
    try:
        with psycopg2.connect(**postgres_conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO customer (name, age, email, purchase, timestamp, store, clerk)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (data['name'], data['age'], data['email'], data['purchase'], data['timestamp'], data['store'], data['clerk']))
                conn.commit()
            print(f"🟢 Postgres: Inserted {data['name']}")
    except Exception as e:
        print(f"❌ Error inserting into Postgres: {e}")

def insert_mariadb(data):
    try:
        with pymysql.connect(**mariadb_conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute("USE mariadb;") # Ensure DB is selected
                cur.execute("""
                    INSERT INTO customer (name, age, email, purchase, timestamp, store, clerk)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (data['name'], data['age'], data['email'], data['purchase'], data['timestamp'], data['store'], data['clerk']))
                conn.commit()
            print(f"🟢 MySQL: Inserted {data['name']}")
    except Exception as e:
        print(f"❌ Error inserting into MySQL: {e}")

# --- Main Loop ---
if __name__ == "__main__":
    print("🇮🇹 Starting Italian Data Generator (Production Ready)...")
    print("⏳ Waiting for databases to launch...")
    time.sleep(15) # Wait for DB containers
    
    # Initialize tables
    create_tables_if_not_exist()
    
    while True:
        random_data_postgres = generate_random_data_postgres()
        random_data_mysql = generate_random_data_mysql()
        
        insert_postgres(random_data_postgres)
        insert_mariadb(random_data_mysql)
        
        sleep_time = random.randint(1, 5)
        print(f"⏳ Next item in {sleep_time} seconds...")
        time.sleep(sleep_time)
