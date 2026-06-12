import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Database Connection
conn = sqlite3.connect(
    r"D:\bluestock_mf_capstone\data\db\bluestock_mf.db"
)

# Load Data
funds_df = pd.read_sql("SELECT * FROM dim_fund", conn)

# Dashboard Title
st.set_page_config(
    page_title="Mutual Fund Analytics Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Mutual Fund Analytics Dashboard")

# KPI Cards
col1, col2 = st.columns(2)

with col1:
    st.metric("Total Funds", len(funds_df))

with col2:
    st.metric("Total Records", funds_df.shape[0])

# Data Preview
st.subheader("Fund Master Data")
st.subheader("Fund Category Distribution")

category_counts = (
    funds_df["category"]
    .value_counts()
    .reset_index()
)

category_counts.columns = ["Category", "Count"]

fig = px.pie(
    category_counts,
    names="Category",
    values="Count",
    title="Funds by Category"
)

st.plotly_chart(fig, use_container_width=True)

st.dataframe(funds_df.head(20))

st.subheader("Top Fund Houses")

fund_house_counts = (
    funds_df["fund_house"]
    .value_counts()
    .head(10)
    .reset_index()
)

fund_house_counts.columns = ["Fund House", "Count"]

fig_bar = px.bar(
    fund_house_counts,
    x="Fund House",
    y="Count",
    title="Top 10 Fund Houses"
)

st.plotly_chart(fig_bar, use_container_width=True)