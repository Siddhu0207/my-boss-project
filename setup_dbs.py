import os
import sqlite3

# Resolve absolute path to the project root directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEV_DB_PATH = os.path.join(BASE_DIR, "dev.db")
SAAS_DB_PATH = os.path.join(BASE_DIR, "saas.db")

# Initialize dev.db
dev_conn = sqlite3.connect(DEV_DB_PATH)
dev_cur = dev_conn.cursor()

# Enable foreign key support
dev_cur.execute("PRAGMA foreign_keys = ON;")

# Create users table
dev_cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    password_hash TEXT NOT NULL
)""")

# Create products table
dev_cur.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    price REAL NOT NULL
)""")

# Create orders table (required by fetch_orders.py)
dev_cur.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
)""")

# Seed users data if empty
dev_cur.execute("SELECT COUNT(*) FROM users")
if dev_cur.fetchone()[0] == 0:
    dev_cur.execute("INSERT INTO users (name, email, password_hash) VALUES ('Alice Johnson', 'alice@example.com', 'hash_pass_123')")
    dev_cur.execute("INSERT INTO users (name, email, password_hash) VALUES ('Bob Smith', 'bob@example.com', 'hash_pass_456')")

# Seed products data if empty
dev_cur.execute("SELECT COUNT(*) FROM products")
if dev_cur.fetchone()[0] == 0:
    dev_cur.execute("INSERT INTO products (product_name, price) VALUES ('Pro Laptop', 1299.99)")
    dev_cur.execute("INSERT INTO products (product_name, price) VALUES ('Wireless Mouse', 29.99)")

# Seed orders data if empty
dev_cur.execute("SELECT COUNT(*) FROM orders")
if dev_cur.fetchone()[0] == 0:
    dev_cur.execute("INSERT INTO orders (user_id, amount) VALUES (1, 299.99)")
    dev_cur.execute("INSERT INTO orders (user_id, amount) VALUES (2, 49.50)")

dev_conn.commit()
dev_conn.close()

# Initialize saas.db
saas_conn = sqlite3.connect(SAAS_DB_PATH)
saas_cur = saas_conn.cursor()

saas_cur.execute("""
CREATE TABLE IF NOT EXISTS subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    org_name TEXT NOT NULL,
    plan_tier TEXT NOT NULL,
    monthly_price REAL NOT NULL
)""")

# Seed saas.db data if empty
saas_cur.execute("SELECT COUNT(*) FROM subscriptions")
if saas_cur.fetchone()[0] == 0:
    saas_cur.execute("INSERT INTO subscriptions (org_name, plan_tier, monthly_price) VALUES ('Acme Corp', 'Enterprise', 499.00)")
    saas_cur.execute("INSERT INTO subscriptions (org_name, plan_tier, monthly_price) VALUES ('Starlight Inc', 'Starter', 49.00)")

saas_conn.commit()
saas_conn.close()

print("✅ Both dev.db and saas.db datasets are ready for pytest!")
