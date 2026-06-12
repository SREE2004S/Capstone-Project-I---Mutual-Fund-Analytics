import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

conn = sqlite3.connect(
    r"D:\bluestock_mf_capstone\data\db\bluestock_mf.db"
)

risk_df = pd.read_sql(
    "SELECT * FROM fact_performance",
    conn
)

st.title("⚠️ Risk Analytics")

st.subheader("Beta Distribution")

fig_beta = px.histogram(
    risk_df,
    x="beta",
    nbins=20,
    title="Distribution of Beta"
)

st.plotly_chart(fig_beta, use_container_width=True)

st.subheader("Risk Grade Breakdown")

risk_grade = (
    risk_df["risk_grade"]
    .value_counts()
    .reset_index()
)

risk_grade.columns = ["Risk Grade", "Count"]

fig_risk = px.pie(
    risk_grade,
    names="Risk Grade",
    values="Count",
    title="Risk Grade Distribution"
)

st.plotly_chart(fig_risk, use_container_width=True)

st.subheader("Top Funds by Maximum Drawdown")

drawdown_df = (
    risk_df.sort_values(
        by="max_drawdown_pct"
    )
    .head(10)
)

fig_dd = px.bar(
    drawdown_df,
    x="scheme_name",
    y="max_drawdown_pct",
    title="Lowest Drawdown Funds"
)

st.plotly_chart(fig_dd, use_container_width=True)

st.subheader("Risk Metrics")

st.dataframe(
    risk_df[
        [
            "scheme_name",
            "beta",
            "sharpe_ratio",
            "std_dev_ann_pct",
            "max_drawdown_pct",
            "risk_grade"
        ]
    ]
)

st.subheader("🏆 Top Recommended Funds")

recommended = risk_df[
    (risk_df["sharpe_ratio"] > 1)
    & (risk_df["beta"] < 1.2)
]

recommended = recommended.sort_values(
    by="sharpe_ratio",
    ascending=False
).head(5)

st.dataframe(
    recommended[
        [
            "scheme_name",
            "category",
            "sharpe_ratio",
            "beta",
            "return_3yr_pct",
            "risk_grade"
        ]
    ]
)

csv = recommended.to_csv(index=False)

st.download_button(
    label="📥 Download Recommendations",
    data=csv,
    file_name="recommended_funds.csv",
    mime="text/csv"
)

st.subheader("⭐ Morningstar Rating Distribution")

rating_df = (
    risk_df["morningstar_rating"]
    .value_counts()
    .reset_index()
)

rating_df.columns = ["Rating", "Count"]

fig_rating = px.bar(
    rating_df,
    x="Rating",
    y="Count",
    title="Morningstar Ratings"
)

st.plotly_chart(fig_rating, use_container_width=True)

