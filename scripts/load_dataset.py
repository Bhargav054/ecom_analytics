import pandas as pd

# File path to your dataset
file_path = r"E:\DataAnalyst projects\ecom-analytics\data\ecom_dataset.csv"

# Load dataset
df = pd.read_csv(file_path)

# Display information
print("✅ Dataset loaded successfully!")
print("\nFirst 5 rows:")
print(df.head())
print("\nShape of dataset:", df.shape)