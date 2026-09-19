import sqlite3

# Initialize dev.db
dev_conn = sqlite3.connect("dev.db")
dev_cur = dev_conn.cursor()

dev_cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    password_hash TEXT NOT NULL
)""")

dev_cur.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    price REAL NOT NULL
)""")

# Seed dev.db data if empty
dev_cur.execute("SELECT COUNT(*) FROM users")
if dev_cur.fetchone()[0] == 0:
    dev_cur.execute("INSERT INTO users (name, email, password_hash) VALUES ('Alice Johnson', 'alice@example.com', 'hash_pass_123')")
    dev_cur.execute("INSERT INTO users (name, email, password_hash) VALUES ('Bob Smith', 'bob@example.com', 'hash_pass_456')")

dev_conn.commit()
dev_conn.close()

# Initialize saas.db
saas_conn = sqlite3.connect("saas.db")
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

saas_conn.commit()
saas_conn.close()

print("✅ Both dev.db and saas.db datasets are ready for pytest!")
