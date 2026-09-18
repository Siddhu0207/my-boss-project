import sqlite3

def fetch_orders_with_users():
    db_path = "dev.db"
    
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # SQL Query to join orders and users to get all orders with the user's name
    query = """
        SELECT 
            orders.id AS order_id,
            users.name AS user_name,
            orders.amount AS order_amount
        FROM orders
        INNER JOIN users ON orders.user_id = users.id;
    """
    
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Display the results in a formatted table
        print(f"{'Order ID':<10} | {'User Name':<15} | {'Amount':<10}")
        print("-" * 43)
        for row in results:
            order_id, user_name, amount = row
            print(f"{order_id:<10} | {user_name:<15} | ${amount:<10.2f}")
            
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the database connection
        conn.close()

if __name__ == "__main__":
    fetch_orders_with_users()
