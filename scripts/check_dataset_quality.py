import pandas as pd

# 1️⃣ Load dataset
file_path = "E:/DataAnalyst projects/ecom-analytics/data/ecom_dataset.csv"
df = pd.read_csv(file_path)

print("✅ Dataset loaded successfully!\n")

# 2️⃣ Basic information
print("🔹 Shape of dataset:", df.shape)
print("\n🔹 Column Names:")
print(df.columns.tolist())

# 3️⃣ Check for missing or null values
print("\n🔍 Missing values per column:")
print(df.isnull().sum())

# 4️⃣ Check for empty strings
empty_counts = (df == "").sum()
print("\n🔍 Empty string counts per column:")
print(empty_counts[empty_counts > 0])

# 5️⃣ Check for numeric columns with zeros
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
if len(numeric_cols) > 0:
    print("\n🔢 Zero counts in numeric columns:")
    for col in numeric_cols:
        zero_count = (df[col] == 0).sum()
        if zero_count > 0:
            print(f"   {col}: {zero_count} zeros")

# 6️⃣ Quick descriptive summary
print("\n📊 Descriptive statistics:")
print(df.describe(include='all').transpose().head(10))
# 7️⃣ Inspect price columns closely
print("\n💰 Sample values from taxful_total_price:")
print(df["taxful_total_price"].head(10))

print("\n💰 Sample values from taxless_total_price:")
print(df["taxless_total_price"].head(10))