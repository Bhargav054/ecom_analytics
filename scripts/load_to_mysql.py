import pandas as pd
import mysql.connector
from mysql.connector import Error
import re

# -------------------------------
# STEP 1: Load Dataset
# -------------------------------
file_path = "data/ecom_dataset.csv"

try:
    df = pd.read_csv(file_path)
    print(f"✅ Dataset loaded successfully with shape: {df.shape}")
except FileNotFoundError:
    print(f"❌ File not found at {file_path}. Please check the path.")
    exit()
except Exception as e:
    print(f"❌ Error loading dataset: {e}")
    exit()

# -------------------------------
# STEP 2: Data Cleaning
# -------------------------------
# Clean 'order_date'
if "order_date" in df.columns:
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce").dt.strftime("%Y-%m-%d %H:%M:%S")
    print("🧹 Cleaned 'order_date' format for MySQL compatibility.")

# Clean money columns
money_cols = ["taxful_total_price", "taxless_total_price"]

for col in money_cols:
    if col in df.columns:
        df[col] = (
            df[col]
            .astype(str)
            .apply(lambda x: re.sub(r"[^0-9.\-]", "", x.strip()) if x.strip() != "" else "0")
            .astype(float)
        )
        print(f"🧹 Cleaned '{col}' column — removed symbols and converted to float.")

# Replace NaNs with empty string
df = df.fillna("")

# Truncate long text fields
if "products" in df.columns:
    df["products"] = df["products"].astype(str).str.slice(0, 5000)

# -------------------------------
# STEP 3: Connect to MySQL
# -------------------------------
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="datauser",
        password="Data@123",
        database="ecom_db"
    )
    cursor = conn.cursor()
    print("✅ Connected to MySQL successfully!")
except Error as e:
    print(f"❌ MySQL Connection Error: {e}")
    exit()

# -------------------------------
# STEP 4: Create Table Dynamically
# -------------------------------
table_name = "orders"

columns = []
for col, dtype in zip(df.columns, df.dtypes):
    if "int" in str(dtype):
        sql_type = "INT"
    elif "float" in str(dtype):
        sql_type = "FLOAT"
    elif "datetime" in str(dtype):
        sql_type = "DATETIME"
    else:
        sql_type = "TEXT"
    columns.append(f"`{col}` {sql_type}")

create_table_query = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    id INT AUTO_INCREMENT PRIMARY KEY,
    {', '.join(columns)}
);
"""

try:
    cursor.execute(create_table_query)
    print(f"✅ Created table '{table_name}' dynamically based on dataset columns.")
except Error as e:
    print(f"❌ Error creating table: {e}")
    conn.close()
    exit()

# -------------------------------
# STEP 5: Insert Data
# -------------------------------
insert_query = f"""
INSERT INTO {table_name} ({', '.join([f'`{c}`' for c in df.columns])})
VALUES ({', '.join(['%s'] * len(df.columns))});
"""

def clean_row(row):
    """Convert values to correct MySQL-friendly types."""
    return tuple(None if str(x).strip() == "" else x for x in row)

try:
    for _, row in df.iterrows():
        cursor.execute(insert_query, clean_row(row))
    conn.commit()
    print(f"✅ Successfully inserted {len(df)} rows into '{table_name}'!")
except Error as e:
    print(f"❌ MySQL Error: {e}")
finally:
    cursor.close()
    conn.close()
    print("🔒 MySQL connection closed.")
