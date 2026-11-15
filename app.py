
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Nassau Candy Analytics",
    page_icon="🍫",
    layout="wide"
)

st.title("🍫 NASSAU CANDY")
st.subheader("Business Profitability & Performance Analytics")

# 1. Load Dataset
df = pd.read_csv("Nassau Candy Distributor.csv")
# 1. Load Dataset
df = pd.read_csv("Nassau Candy Distributor.csv")

# Filters
st.sidebar.header("Filters")

selected_region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

selected_division = st.sidebar.multiselect(
    "Select Division",
    options=df["Division"].unique(),
    default=df["Division"].unique()
)

df = df[
    (df["Region"].isin(selected_region)) &
    (df["Division"].isin(selected_division))
]

st.success("Dataset Loaded Successfully!")
st.success("Dataset Loaded Successfully!")


# 2. Dataset Overview
st.subheader("📊 Dataset Overview")

st.write("Total Rows:", df.shape[0])
st.write("Total Columns:", df.shape[1])
st.write("Column Names:", df.columns.tolist())
st.write("Missing Values:", df.isnull().sum())
st.write("Statistical Summary:")
st.write(df.describe())

# 3. Business Performance KPIs
st.subheader("📈 Business Performance")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Sales", f"${df['Sales'].sum():,.2f}")

with col2:
    st.metric("Total Profit", f"${df['Gross Profit'].sum():,.2f}")

with col3:
    st.metric("Total Cost", f"${df['Cost'].sum():,.2f}")

with col4:
    st.metric("Total Units", f"{df['Units'].sum():,}")

# 4. Region-wise Sales
st.subheader("🌍 Region-wise Sales Analysis")

region_sales = df.groupby("Region")["Sales"].sum().reset_index()

fig1 = px.bar(
    region_sales,
    x="Region",
    y="Sales",
    color="Region",
    title="Total Sales by Region"
)

st.plotly_chart(fig1, use_container_width=True)

# 5. Division-wise Profit
st.subheader("🏭 Division-wise Profit Analysis")

division_profit = df.groupby("Division")["Gross Profit"].sum().reset_index()

fig2 = px.bar(
    division_profit,
    x="Division",
    y="Gross Profit",
    color="Division",
    title="Total Profit by Division"
)

st.plotly_chart(fig2, use_container_width=True)

# 6. Top 10 Profitable Products
st.subheader("🍫 Top 10 Profitable Products")

product_profit = (
    df.groupby("Product Name")["Gross Profit"]
    .sum()
    .reset_index()
    .sort_values(by="Gross Profit", ascending=False)
    .head(10)
)

fig3 = px.bar(
    product_profit,
    x="Gross Profit",
    y="Product Name",
    orientation="h",
    color="Gross Profit",
    title="Top 10 Products by Gross Profit"
)

st.plotly_chart(fig3, use_container_width=True)

# 7. Monthly Sales Trend
st.subheader("📅 Monthly Sales Trend")

df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")

df["Month"] = df["Order Date"].dt.to_period("M").astype(str)

monthly_sales = (
    df.groupby("Month")["Sales"]
    .sum()
    .reset_index()
)

fig4 = px.line(
    monthly_sales,
    x="Month",
    y="Sales",
    markers=True,
    title="Monthly Sales Performance"
)

st.plotly_chart(fig4, use_container_width=True)

# 8. Division-wise Profit Margin
st.subheader("💰 Gross Profit Margin Analysis")

margin_data = (
    df.groupby("Division")[["Sales", "Gross Profit"]]
    .sum()
    .reset_index()
)

margin_data["Profit Margin (%)"] = (
    margin_data["Gross Profit"] /
    margin_data["Sales"].replace(0, float("nan")) * 100
)

fig5 = px.bar(
    margin_data,
    x="Division",
    y="Profit Margin (%)",
    color="Division",
    title="Profit Margin by Division",
    text_auto=".2f"
)

st.plotly_chart(fig5, use_container_width=True)

# 9. Cost vs Profit
st.subheader("💹 Cost vs Profit Analysis")

cost_profit = (
    df.groupby("Division")[["Cost", "Gross Profit"]]
    .sum()
    .reset_index()
)

fig6 = px.bar(
    cost_profit,
    x="Division",
    y=["Cost", "Gross Profit"],
    barmode="group",
    title="Cost vs Gross Profit by Division",
    labels={"value": "Amount", "variable": "Metric"}
)

st.plotly_chart(fig6, use_container_width=True)

# 10. Top 10 Best Selling Products
st.subheader("📦 Top 10 Best Selling Products")

top_products = (
    df.groupby("Product Name")["Units"]
    .sum()
    .reset_index()
    .sort_values(by="Units", ascending=False)
    .head(10)
)

fig7 = px.bar(
    top_products,
    x="Units",
    y="Product Name",
    orientation="h",
    color="Units",
    title="Top 10 Products by Units Sold"
)

st.plotly_chart(fig7, use_container_width=True)

# 11. Division-wise Sales Contribution
st.subheader("🥧 Division-wise Sales Contribution")

division_sales = (
    df.groupby("Division")["Sales"]
    .sum()
    .reset_index()
)

fig8 = px.pie(
    division_sales,
    names="Division",
    values="Sales",
    title="Sales Contribution by Division",
    hole=0.4
)

st.plotly_chart(fig8, use_container_width=True)

# 12. Region-wise Profit Margin
st.subheader("📊 Region-wise Gross Profit Margin")

region_margin = (
    df.groupby("Region")[["Sales", "Gross Profit"]]
    .sum()
    .reset_index()
)

region_margin["Profit Margin (%)"] = (
    region_margin["Gross Profit"] /
    region_margin["Sales"].replace(0, float("nan")) * 100
)

fig9 = px.bar(
    region_margin,
    x="Region",
    y="Profit Margin (%)",
    color="Region",
    title="Gross Profit Margin by Region",
    text_auto=".2f"
)

st.plotly_chart(fig9, use_container_width=True)

# 13. Business Insights
st.subheader("💡 Key Business Insights")

best_region = df.groupby("Region")["Sales"].sum().idxmax()

best_division = df.groupby("Division")["Gross Profit"].sum().idxmax()

best_product = df.groupby("Product Name")["Gross Profit"].sum().idxmax()

overall_margin = (
    df["Gross Profit"].sum() /
    df["Sales"].sum() * 100
)

st.write("🏆 Highest Sales Region:", best_region)
st.write("💰 Most Profitable Division:", best_division)
st.write("🍫 Most Profitable Product:", best_product)
st.write("📊 Overall Profit Margin:", f"{overall_margin:.2f}%")

# 14. Download Dataset
st.subheader("📥 Download Dataset")

csv_data = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Nassau Candy Dataset",
    data=csv_data,
    file_name="Nassau_Candy_Analysis.csv",
    mime="text/csv"
)

# 15. Complete Dataset
st.subheader("📋 Complete Dataset")

st.dataframe(
    df,
    use_container_width=True,
    height=500
)

# 16. Project Information
st.divider()

st.subheader("🍫 About This Project")

st.write("""
This dashboard analyses Nassau Candy Distributor's business performance.

The analysis focuses on:
- Sales Performance
- Gross Profit Analysis
- Regional Performance
- Product Profitability
- Monthly Sales Trends
- Business Insights
""")

st.caption("Developed by Vivek Kumar | Data Analytics Project")
