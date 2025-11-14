# scripts/dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector
from mysql.connector import Error
from datetime import datetime

st.set_page_config(page_title="E-commerce Analytics Dashboard", layout="wide")

# -------------------------
# Config / DB connection
# -------------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "datauser",
    "password": "Data@123",
    "database": "ecom_db"
}

@st.cache_data(ttl=300)
def load_orders_from_db():
    """Load entire orders table into a DataFrame and clean column names."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        # load whole table
        df = pd.read_sql_query("SELECT * FROM orders;", conn)
        conn.close()
    except Exception as e:
        st.error(f"Error loading data from MySQL: {e}")
        return pd.DataFrame()

    # normalize column names (replace dots with underscores)
    df.columns = [c.replace(".", "_") for c in df.columns]

    # convert order_date if present
    if "order_date" in df.columns:
        df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

    # ensure numeric columns are numeric
    for col in ["taxful_total_price", "taxless_total_price", "total_quantity"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)

    # some columns might contain lists as strings; keep as-is for now
    return df

# Load data
df = load_orders_from_db()

if df.empty:
    st.title("E-commerce Analytics Dashboard")
    st.warning("No data found in the 'orders' table. Please run the ETL to load data first.")
    st.stop()

# -------------------------
# Sidebar filters
# -------------------------
st.sidebar.header("Filters")

# Date range
min_date = df["order_date"].min()
max_date = df["order_date"].max()
date_range = st.sidebar.date_input("Order date range", value=(min_date.date(), max_date.date()),
                                   min_value=min_date.date(), max_value=max_date.date())

# Country filter - handle both possible names
country_col_candidates = [c for c in df.columns if "geoip" in c and "country" in c]
country_col = country_col_candidates[0] if country_col_candidates else None
countries = sorted(df[country_col].dropna().unique().tolist()) if country_col else []
selected_countries = st.sidebar.multiselect("Country", options=countries, default=countries)

# Category filter
category_list = sorted(df["category"].dropna().unique().tolist()) if "category" in df.columns else []
selected_categories = st.sidebar.multiselect("Category", options=category_list, default=category_list)

# Customer search
customer_search = st.sidebar.text_input("Customer name contains")

# Apply filters to a working dataframe
filtered = df.copy()
# date filtering
start, end = date_range
filtered = filtered[(filtered["order_date"].dt.date >= start) & (filtered["order_date"].dt.date <= end)]
# country
if country_col and selected_countries:
    filtered = filtered[filtered[country_col].isin(selected_countries)]
# category - categories in this dataset might be stringified lists; filter with substring
if selected_categories:
    filtered = filtered[filtered["category"].apply(lambda x: any(cat in str(x) for cat in selected_categories))]
# customer search
if customer_search:
    filtered = filtered[filtered["customer_full_name"].str.contains(customer_search, case=False, na=False)]

# -------------------------
# Top-level KPIs
# -------------------------
st.title("🛒 E-commerce Analytics Dashboard")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

total_revenue = filtered["taxful_total_price"].sum()
total_orders = filtered.shape[0]
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
total_unique_customers = filtered["customer_id"].nunique() if "customer_id" in filtered.columns else filtered["customer_full_name"].nunique()

kpi1.metric("Total Revenue", f"{total_revenue:,.2f}")
kpi2.metric("Total Orders", f"{total_orders:,}")
kpi3.metric("Avg Order Value", f"{avg_order_value:,.2f}")
kpi4.metric("Unique Customers", f"{total_unique_customers:,}")

st.markdown("---")

# -------------------------
# Tabs for dashboards
# -------------------------
tab_overview, tab_customers, tab_products, tab_data = st.tabs([
    "Overview", "Customer Insights", "Product Performance", "Data Explorer"
])

# -------------------------
# Overview Tab
# -------------------------
with tab_overview:
    st.subheader("Overview")

    # Sales by country
    if country_col:
        agg_country = (filtered.groupby(country_col)
                               .agg(total_sales=("taxful_total_price", "sum"),
                                    total_orders=("order_id", "count") if "order_id" in filtered.columns else ("taxful_total_price","count"))
                               .reset_index()
                               .sort_values("total_sales", ascending=False))
        fig_country = px.bar(agg_country, x=country_col, y="total_sales", title="Sales by Country", text_auto=".2s")
        st.plotly_chart(fig_country, use_container_width=True)
    else:
        st.info("Country column not found in dataset.")

    # Monthly revenue
    if "order_date" in filtered.columns:
        monthly = (filtered.groupby(filtered["order_date"].dt.to_period("M"))
                          .agg(monthly_revenue=("taxful_total_price", "sum"))
                          .reset_index())
        monthly["order_date"] = monthly["order_date"].dt.strftime("%Y-%m")
        fig_month = px.line(monthly, x="order_date", y="monthly_revenue", title="Monthly Revenue", markers=True)
        fig_month.update_layout(xaxis_title="Month", yaxis_title="Revenue")
        st.plotly_chart(fig_month, use_container_width=True)
    else:
        st.info("order_date column not found in dataset.")

    # Top categories
    if "category" in filtered.columns:
        # categories may be lists stored as strings; aggregate by string
        cat_agg = filtered.groupby("category").agg(total_sales=("taxful_total_price", "sum")).reset_index().sort_values("total_sales", ascending=False).head(10)
        fig_cat = px.bar(cat_agg, x="category", y="total_sales", title="Top Categories by Revenue", text_auto=True)
        st.plotly_chart(fig_cat, use_container_width=True)

# -------------------------
# Customer Insights Tab
# -------------------------
with tab_customers:
    st.subheader("Customer Insights")

    # Top customers
    top_customers = (filtered.groupby("customer_full_name")
                               .agg(total_spent=("taxful_total_price", "sum"),
                                    orders=("order_id", "count") if "order_id" in filtered.columns else ("taxful_total_price","count"))
                               .reset_index()
                               .sort_values("total_spent", ascending=False).head(20))
    st.markdown("**Top Customers**")
    st.dataframe(top_customers, use_container_width=True)
    fig_cust = px.bar(top_customers.head(10), x="customer_full_name", y="total_spent", title="Top 10 Customers by Spend")
    st.plotly_chart(fig_cust, use_container_width=True)

    # Gender split (if present)
    if "customer_gender" in filtered.columns:
        gender = filtered["customer_gender"].value_counts().reset_index()
        gender.columns = ["gender", "count"]
        fig_gender = px.pie(gender, names="gender", values="count", title="Gender Distribution")
        st.plotly_chart(fig_gender, use_container_width=True)
    else:
        st.info("No 'customer_gender' column available.")

# -------------------------
# Product Performance Tab
# -------------------------
with tab_products:
    st.subheader("Product Performance")

    # Top SKUs / manufacturers
    if "sku" in filtered.columns:
        sku_agg = filtered.groupby("sku").agg(total_sales=("taxful_total_price","sum"), qty=("total_quantity","sum")).reset_index().sort_values("total_sales", ascending=False).head(20)
        st.dataframe(sku_agg, use_container_width=True)
        fig_sku = px.bar(sku_agg.head(10), x="sku", y="total_sales", title="Top SKUs by Revenue")
        st.plotly_chart(fig_sku, use_container_width=True)

    if "manufacturer" in filtered.columns:
        man_agg = filtered.groupby("manufacturer").agg(total_sales=("taxful_total_price","sum")).reset_index().sort_values("total_sales", ascending=False).head(10)
        fig_man = px.bar(man_agg, x="manufacturer", y="total_sales", title="Top Manufacturers by Revenue")
        st.plotly_chart(fig_man, use_container_width=True)

# -------------------------
# Data Explorer Tab
# -------------------------
with tab_data:
    st.subheader("Data Explorer")
    st.markdown("Filter, search and export the filtered dataset below.")

    st.write(f"Showing {filtered.shape[0]} rows after filters.")
    st.dataframe(filtered, use_container_width=True)

    # Export filtered dataset
    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download filtered data as CSV", data=csv, file_name="filtered_orders.csv", mime="text/csv")

# -------------------------
# Footer
# -------------------------
st.markdown("---")
st.caption("Project by Bhargav Ummireddi - Data Analyst Portfolio")

