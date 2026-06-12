import sqlite3
import pandas as pd
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ====================================
# DATABASE CONNECTION
# ====================================

conn = sqlite3.connect(
    r"D:\bluestock_mf_capstone\data\db\bluestock_mf.db"
)

# ====================================
# LOAD TOP FUNDS
# ====================================

query = """
SELECT
    scheme_name,
    return_3yr_pct,
    sharpe_ratio,
    aum_crore
FROM fact_performance
ORDER BY return_3yr_pct DESC
LIMIT 10
"""

df = pd.read_sql(query, conn)

conn.close()

# ====================================
# GENERATE HTML TABLE
# ====================================

html_table = df.to_html(
    index=False,
    border=1
)

# ====================================
# EMAIL BODY
# ====================================

html_body = f"""
<html>
<head>
<style>
table {{
    border-collapse: collapse;
}}

th, td {{
    padding: 8px;
    border: 1px solid black;
}}
</style>
</head>

<body>

<h2>Weekly Mutual Fund Performance Report</h2>

<p>Top 10 Funds Based on 3-Year Returns</p>

{html_table}

</body>
</html>
"""

# ====================================
# EMAIL SETTINGS
# ====================================

sender_email = "srinivasan2004ss@gmail.com"

receiver_email = "srinivasan2004ss@gmail.com"

app_password = "hvmz kvgj blwc fsxm"

# ====================================
# CREATE EMAIL
# ====================================

message = MIMEMultipart("alternative")

message["Subject"] = "Weekly Mutual Fund Performance Report"

message["From"] = sender_email

message["To"] = receiver_email

message.attach(
    MIMEText(
        html_body,
        "html"
    )
)

# ====================================
# SEND EMAIL
# ====================================

server = smtplib.SMTP(
    "smtp.gmail.com",
    587
)

server.starttls()

server.login(
    sender_email,
    app_password
)

server.sendmail(
    sender_email,
    receiver_email,
    message.as_string()
)

server.quit()

print("Email Sent Successfully")

