import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

conn = sqlite3.connect(
    r"D:\bluestock_mf_capstone\data\db\bluestock_mf.db"
)

perf_df = pd.read_sql(
    "SELECT * FROM fact_performance",
    conn
)

st.title("📈 Performance Analytics")

top_sharpe = (
    perf_df.sort_values(
        by="sharpe_ratio",
        ascending=False
    )
    .head(10)
)

fig = px.bar(
    top_sharpe,
    x="scheme_name",
    y="sharpe_ratio",
    title="Top 10 Funds by Sharpe Ratio"
)

st.plotly_chart(fig, use_container_width=True)

st.dataframe(top_sharpe)

st.subheader("Risk vs Return Analysis")

fig_scatter = px.scatter(
    perf_df,
    x="std_dev_ann_pct",
    y="return_3yr_pct",
    size="aum_crore",
    color="category",
    hover_name="scheme_name",
    title="Risk vs Return (3-Year)"
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.subheader("Top 10 Funds by 3-Year Return")

top_return = (
    perf_df.sort_values(
        by="return_3yr_pct",
        ascending=False
    )
    .head(10)
)

fig_return = px.bar(
    top_return,
    x="scheme_name",
    y="return_3yr_pct",
    title="Top 10 Funds by 3-Year Return"
)

st.plotly_chart(fig_return, use_container_width=True)