📦 E-Commerce Analytics Project
End-to-End Data Engineering + Analytics + Dashboarding Project

This project is a complete E-commerce Analytics Pipeline built using:
🔹 Python for data cleaning & ETL
🔹 MySQL for database storage
🔹 Streamlit for interactive dashboards
🔹 Power BI for business insights
🔹 Git & GitHub for version control

It transforms raw E-commerce sales data into insights such as:
✔️ Revenue trends
✔️ Country-wise sales
✔️ Top products
✔️ Monthly revenue
✔️ Customer behavior
✔️ Order patterns

🚀 Project Architecture

               +---------------------+
               |  Raw CSV Dataset    |
               +----------+----------+
                          |
                          v
                 Python ETL Scripts
        (cleaning, formatting, preprocessing)
                          |
                          v
               +----------------------+
               |  MySQL Database      |
               |  (orders table)      |
               +----------+-----------+
                          |
        +-----------------+--------------------+
        |                                      |
        v                                      v
  Streamlit Dashboard                   Power BI Dashboard
 (real-time analytics)               (business intelligence)

📁 Folder Structure
ecom-analytics/
│
├── data/
│   └── ecom_dataset.csv
│
├── scripts/
│   ├── load_dataset.py
│   ├── load_to_mysql.py
│   ├── analyze_views.py
│   ├── dashboard.py
│   ├── test_mysql_conn.py
│   ├── generate_mock_sales.py
│   └── check_dataset_quality.py
│
├── mysqlworkbench/
│   ├── db creation.txt
│   └── user privileges.txt
│
├── README.md
└── requirements.txt

🛠️ Tech Stack
Category	Tools Used
Programming	Python
Database	MySQL
Dashboard	Streamlit, Power BI
Libraries	pandas, plotly, mysql-connector
Version Control	Git & GitHub


🧹 Data Cleaning & Transformation

Key preprocessing steps performed:
Handling missing values
Cleaning numeric fields (price, taxful_total_price)
Extracting date parts (month, year)
Fixing inconsistent data types
Normalizing product, customer, and geo details
Fixing currency symbols and encoding issues

🗄️ Database Setup (MySQL)
1️⃣ Create the database
CREATE DATABASE ecom_analytics;

2️⃣ Create MySQL user (recommended for project security)
CREATE USER 'datauser'@'localhost' IDENTIFIED BY 'Data@123';
GRANT ALL PRIVILEGES ON ecom_analytics.* TO 'datauser'@'localhost';
FLUSH PRIVILEGES;

3️⃣ Verify user login (optional)
mysql -u datauser -p

4️⃣ Load the dataset into MySQL
Run this Python script:
python scripts/load_to_mysql.py

This script will:
✔ Clean the dataset
✔ Fix dates & currencies
✔ Automatically generate the orders table
✔ Insert all rows into MySQL

5️⃣ Validate data loaded correctly
Total Rows:
SELECT COUNT(*) FROM orders;

Total Revenue:
SELECT SUM(taxful_total_price) FROM orders;

Sample:
SELECT * FROM orders LIMIT 10;

📌 Future Enhancements
Add scheduling with Airflow
Add Docker support
Deploy Streamlit on cloud
Add automated data quality checks
Log-based monitoring

