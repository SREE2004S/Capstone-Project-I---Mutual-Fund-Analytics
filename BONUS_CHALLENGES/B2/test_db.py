import sqlite3
import pandas as pd

conn = sqlite3.connect(
    r"D:\bluestock_mf_capstone\data\db\bluestock_mf.db"
)

df = pd.read_sql(
    "SELECT * FROM fact_performance LIMIT 5",
    conn
)

print(df.columns.tolist())
print(df.head())

conn.close()