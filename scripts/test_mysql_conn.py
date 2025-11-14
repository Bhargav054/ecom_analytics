import mysql.connector
from mysql.connector import Error

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="ecom_user",
        password="ecom_pass",
        database="ecom_db"
    )
    if conn.is_connected():
        print("✅ Connected to MySQL successfully!")
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print("Current database:", record)
        conn.close()
except Error as e:
    print("❌ Connection failed:", e)