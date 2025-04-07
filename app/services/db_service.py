# app/services/db_service.py

import sqlite3

def get_orders_by_user(user_id: str) -> str:
    conn = sqlite3.connect("your_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT order_id, product, order_date FROM orders WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return "No orders found."
    
    # Format rows into readable text for the LLM
    return "\n".join([f"Order ID: {r[0]}, Product: {r[1]}, Date: {r[2]}" for r in rows])
