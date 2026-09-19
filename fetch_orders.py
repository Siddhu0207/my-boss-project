import os
import sqlite3

# Resolve absolute path relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "dev.db")

def fetch_orders_with_users():
    query = """
        SELECT 
            orders.id AS order_id,
            users.name AS user_name,
            orders.amount AS order_amount
        FROM orders
        INNER JOIN users ON orders.user_id = users.id;
    """
    
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        
        if not results:
            print("No orders found.")
            return

        # Display the formatted table
        print(f"{'Order ID':<10} | {'User Name':<15} | {'Amount':<10}")
        print("-" * 43)
        for order_id, user_name, amount in results:
            formatted_amount = f"${amount:.2f}" if isinstance(amount, (int, float)) else str(amount)
            print(f"{order_id:<10} | {user_name:<15} | {formatted_amount:<10}")
            
    except sqlite3.Error as e:
        print(f"Database Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    fetch_orders_with_users()
