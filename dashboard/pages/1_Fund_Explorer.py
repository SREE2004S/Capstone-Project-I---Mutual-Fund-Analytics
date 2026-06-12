import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect(
    r"D:\bluestock_mf_capstone\data\db\bluestock_mf.db"
)

funds_df = pd.read_sql(
    "SELECT * FROM dim_fund",
    conn
)

st.title("🔎 Fund Explorer")

search = st.text_input("Search Fund")

if search:
    filtered = funds_df[
        funds_df["scheme_name"].str.contains(
            search,
            case=False,
            na=False
        )
    ]
else:
    filtered = funds_df

st.dataframe(filtered)