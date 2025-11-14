"""
import pandas as pd
import random
from datetime import datetime, timedelta
import mysql.connector

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="datauser",
    password="Data@123",
    database="ecom_db"   # change if your DB name is different
)
cursor = conn.cursor()

# Generate mock sales for 6 months
start_date = datetime(2019, 1, 1)
months = ["2019-01", "2019-02", "2019-03", "2019-04", "2019-05", "2019-06"]
rows = []

for month in months:
    # random number of orders per month
    num_orders = random.randint(20, 50)
    for i in range(num_orders):
        order_date = start_date + timedelta(days=random.randint(0, 27))
        rows.append({
            "category": random.choice(["Electronics", "Clothing", "Home", "Toys", "Books"]),
            "currency": "USD",
            "customer_first_name": random.choice(["John", "Alice", "Mark", "Sophia", "David"]),
            "customer_full_name": "",
            "customer_gender": random.choice(["M", "F"]),
            "customer_id": random.randint(1000, 9999),
            "customer_last_name": random.choice(["Smith", "Johnson", "Brown", "Lee"]),
            "customer_phone": None,
            "day_of_week": order_date.strftime("%A"),
            "day_of_week_i": order_date.weekday(),
            "email": f"user{random.randint(1000,9999)}@example.com",
            "geoip.city_name": random.choice(["New York", "Los Angeles", "London", "Paris", "Dubai"]),
            "geoip.continent_name": "North America",
            "geoip.country_iso_code": random.choice(["US", "GB", "AE", "FR", "CA"]),
            "geoip.location": "",
            "geoip.region_name": "",
            "manufacturer": random.choice(["BrandA", "BrandB", "BrandC"]),
            "order_date": order_date.strftime("%Y-%m-%d"),
            "order_id": random.randint(10000, 99999),
            "products": "Sample Product",
            "products.created_on": order_date.strftime("%Y-%m-%d"),
            "sku": f"SKU{random.randint(1000,9999)}",
            "taxful_total_price": round(random.uniform(50, 500), 2),
            "taxless_total_price": round(random.uniform(40, 480), 2),
            "total_quantity": random.randint(1, 5),
            "total_unique_products": random.randint(1, 3),
            "type": "order",
            "user": random.choice(["online", "mobile", "instore"]),
        })

# Convert to DataFrame
df = pd.DataFrame(rows)

# Insert into MySQL
cols = ", ".join([f"`{c}`" for c in df.columns])
placeholders = ", ".join(["%s"] * len(df.columns))
insert_query = f"INSERT INTO orders ({cols}) VALUES ({placeholders})"

for _, row in df.iterrows():
    cursor.execute(insert_query, tuple(row))

conn.commit()
print(f"✅ Inserted {len(df)} mock rows into 'orders' table successfully!")
cursor.close()
conn.close()
"""
#####################################################################
import mysql.connector
import random
from datetime import datetime, timedelta

# --------------------------
# MySQL Connection
# --------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="datauser",
    password="Data@123",
    database="ecom_db"   # ✅ use your actual DB name here
)
cursor = conn.cursor()

# --------------------------
# Configuration
# --------------------------
countries = ["US", "AE", "EG", "FR", "GB", "MA", "MC", "SA", "CO", "TR"]
categories = [
    "Men's Clothing", "Women's Clothing", "Men's Shoes",
    "Women's Shoes", "Accessories", "Electronics"
]
manufacturers = ["Nike", "Adidas", "Puma", "Apple", "Samsung", "Sony"]

# Random monthly variation factors
month_factors = {
    1: 0.7,   # January - low season
    2: 0.8,
    3: 1.2,   # March - sales boost
    4: 1.0,
    5: 1.1,
    6: 0.9,
    7: 1.4,   # July - summer peak
    8: 1.3,
    9: 1.0,
    10: 0.8,
    11: 1.5,  # November - Black Friday
    12: 1.6   # December - holidays
}

# --------------------------
# Generate mock orders
# --------------------------
mock_data = []
start_date = datetime(2019, 1, 1)

for i in range(1, 301):  # 300 rows for realism
    country = random.choice(countries)
    category = random.choice(categories)
    manufacturer = random.choice(manufacturers)
    order_date = start_date + timedelta(days=random.randint(0, 365 * 2))  # 2019–2020
    base_price = round(random.uniform(20, 250), 2)
    quantity = random.randint(1, 5)
    total = round(base_price * quantity, 2)
    month_factor = month_factors.get(order_date.month, 1.0)
    total = round(total * month_factor, 2)

    mock_data.append((
        category,
        manufacturer,
        country,
        order_date.strftime("%Y-%m-%d"),
        quantity,
        total
    ))

# --------------------------
# Insert mock data
# --------------------------
insert_query = """
INSERT INTO orders (category, manufacturer, `geoip.country_iso_code`, order_date, total_quantity, taxful_total_price)
VALUES (%s, %s, %s, %s, %s, %s)
"""

cursor.executemany(insert_query, mock_data)
conn.commit()

print(f"✅ Inserted {cursor.rowcount} mock rows into 'orders' table successfully!")

# --------------------------
# Close connection
# --------------------------
cursor.close()
conn.close()
print("🔒 MySQL connection closed.")
