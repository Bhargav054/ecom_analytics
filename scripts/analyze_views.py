import pandas as pd
import plotly.express as px
import mysql.connector
from mysql.connector import Error

# -------------------------------
# STEP 1: Connect to MySQL
# -------------------------------
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="datauser",
        password="Data@123",
        database="ecom_db"
    )
    print("✅ Connected to MySQL successfully!")
except Error as e:
    print(f"❌ MySQL Connection Error: {e}")
    exit()

# Helper function to run queries and return a dataframe
def run_query(query):
    print(f"\n📊 Running query:\n{query}\n")
    return pd.read_sql(query, conn)

# -------------------------------
# STEP 2: Define and Run Analysis Queries
# -------------------------------

# 1️⃣ Total Sales by Country
query1 = """
SELECT 
    `geoip.country_iso_code` AS country,
    SUM(taxful_total_price) AS total_sales
FROM orders
GROUP BY `geoip.country_iso_code`
ORDER BY total_sales DESC;
"""
df_country = run_query(query1)

# 2️⃣ Top 10 Customers by Spending
query2 = """
SELECT 
    customer_full_name AS customer,
    SUM(taxful_total_price) AS total_spent
FROM orders
GROUP BY customer_full_name
ORDER BY total_spent DESC
LIMIT 10;
"""
df_customers = run_query(query2)

# 3️⃣ Monthly Revenue Trend
query3 = """
SELECT 
    DATE_FORMAT(order_date, '%Y-%m') AS month,
    SUM(taxful_total_price) AS monthly_revenue
FROM orders
GROUP BY month
ORDER BY month;
"""
df_monthly = run_query(query3)

# 4️⃣ Top Product Categories
query4 = """
SELECT 
    category,
    SUM(total_quantity) AS total_quantity_sold,
    SUM(taxful_total_price) AS total_revenue
FROM orders
GROUP BY category
ORDER BY total_revenue DESC
LIMIT 10;
"""
df_categories = run_query(query4)

# -------------------------------
# STEP 3: Generate Visualizations
# -------------------------------

print("\n📈 Generating interactive charts...\n")

# 1️⃣ Sales by Country
fig1 = px.bar(df_country, x="country", y="total_sales", title="Sales by Country", color="total_sales", text_auto=True)
fig1.show()

# 2️⃣ Top 10 Customers
fig2 = px.bar(df_customers, x="customer", y="total_spent", title="Top 10 Customers by Spending", color="total_spent", text_auto=True)
fig2.show()

# 3️⃣ Monthly Revenue Trend
fig3 = px.line(df_monthly, x="month", y="monthly_revenue", title="Monthly Revenue Trend", markers=True)
fig3.show()

# 4️⃣ Top Product Categories
fig4 = px.bar(df_categories, x="category", y="total_revenue", title="Top Product Categories", color="total_revenue", text_auto=True)
fig4.show()

print("\n✅ All visualizations generated successfully!")
conn.close()
