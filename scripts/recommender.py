"""
Bluestock Mutual Fund Capstone
Advanced Analytics & Recommender

Author: Srinivasan S
"""

from pathlib import Path
import pandas as pd
import numpy as np
import logging
import matplotlib.pyplot as plt

# =====================================================
# LOGGING
# =====================================================

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "recommender.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logging.info(
    "Recommender Started"
)

# =====================================================
# PATHS
# =====================================================

PROCESSED_DIR = Path(
    "data/processed"
)

REPORT_DIR = Path(
    "reports"
)

REPORT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

plt.savefig(
    REPORT_DIR /
    "rolling_sharpe_chart.png",
    dpi=300
)
# =====================================================
# INPUT FILES
# =====================================================

NAV_FILE = (
    PROCESSED_DIR /
    "nav_history_clean.csv"
)

PERFORMANCE_FILE = (
    PROCESSED_DIR /
    "performance_clean.csv"
)

SCORECARD_FILE = (
    PROCESSED_DIR /
    "fund_scorecard.csv"
)

# =====================================================
# LOAD DATA
# =====================================================

print(
    "Loading datasets..."
)

nav = pd.read_csv(
    NAV_FILE
)

performance = pd.read_csv(
    PERFORMANCE_FILE
)

scorecard = pd.read_csv(
    SCORECARD_FILE
)

nav["date"] = pd.to_datetime(
    nav["date"]
)

logging.info(
    "Datasets loaded"
)
TRANSACTION_FILE = (
    PROCESSED_DIR /
    "transactions_clean.csv"
)

HOLDINGS_FILE = (
    PROCESSED_DIR /
    "holdings_clean.csv"
)

transactions = pd.read_csv(
    TRANSACTION_FILE
)

holdings = pd.read_csv(
    HOLDINGS_FILE
)

transactions["transaction_date"] = (
    pd.to_datetime(
        transactions["transaction_date"]
    )
)
# =====================================================
# DAILY RETURNS
# =====================================================

nav = nav.sort_values(
    ["amfi_code", "date"]
)

nav["daily_return"] = (
    nav.groupby("amfi_code")
    ["nav"]
    .pct_change()
)

logging.info(
    "Daily returns created"
)

# =====================================================
# VAR & CVAR
# =====================================================

results = []

for fund_code in nav[
    "amfi_code"
].unique():

    fund_df = nav[
        nav["amfi_code"]
        == fund_code
    ]

    returns = (
        fund_df[
            "daily_return"
        ]
        .dropna()
    )

    if len(returns) < 30:
        continue

    var_95 = np.percentile(
        returns,
        5
    )

    cvar_95 = (
        returns[
            returns <= var_95
        ]
        .mean()
    )

    results.append({

        "amfi_code":
        fund_code,

        "var_95_pct":
        round(
            var_95 * 100,
            2
        ),

        "cvar_95_pct":
        round(
            cvar_95 * 100,
            2
        )

    })

risk_df = pd.DataFrame(
    results
)

logging.info(
    "VaR and CVaR calculated"
)

# =====================================================
# RISK CLASSIFICATION
# =====================================================

def classify_risk(var):

    if var > -1:
        return "Low Risk"

    elif var > -2:
        return "Moderate Risk"

    else:
        return "High Risk"

risk_df["risk_bucket"] = (
    risk_df["var_95_pct"]
    .apply(
        classify_risk
    )
)

# =====================================================
# RECOMMENDATION ENGINE
# =====================================================

recommendations = (
    scorecard.merge(
        risk_df,
        on="amfi_code"
    )
)

recommendations = (
    recommendations
    .sort_values(
        "fund_score",
        ascending=False
    )
)

logging.info(
    "Recommendations created"
)

# =====================================================
# LOW RISK
# =====================================================

low_risk = recommendations[
    recommendations[
        "risk_bucket"
    ]
    ==
    "Low Risk"
].head(5)

# =====================================================
# MODERATE RISK
# =====================================================

moderate_risk = recommendations[
    recommendations[
        "risk_bucket"
    ]
    ==
    "Moderate Risk"
].head(5)

# =====================================================
# HIGH RISK
# =====================================================

high_risk = recommendations[
    recommendations[
        "risk_bucket"
    ]
    ==
    "High Risk"
].head(5)

# =====================================================
# EXPORT FILES
# =====================================================

risk_df.to_csv(
    PROCESSED_DIR /
    "var_cvar_report.csv",
    index=False
)

recommendations.to_csv(
    PROCESSED_DIR /
    "recommendations.csv",
    index=False
)

logging.info(
    "Files exported"
)

# =====================================================
# SUMMARY
# =====================================================

print("=" * 60)
print(
    "ADVANCED ANALYTICS COMPLETED"
)
print("=" * 60)

print(
    "Generated Files:"
)

print(
    "- var_cvar_report.csv"
)

print(
    "- recommendations.csv"
)

logging.info(
    "Recommender completed"
)

# =====================================================
# ROLLING SHARPE
# =====================================================

import matplotlib.pyplot as plt

top5_funds = (
    scorecard
    .head(5)
    ["amfi_code"]
    .tolist()
)

plt.figure(
    figsize=(12,6)
)

for fund_code in top5_funds:

    fund_df = nav[
        nav["amfi_code"]
        == fund_code
    ].copy()

    returns = (
        fund_df["daily_return"]
    )

    rolling_sharpe = (

        returns
        .rolling(90)
        .mean()

        /

        returns
        .rolling(90)
        .std()

    ) * np.sqrt(252)

    plt.plot(
        fund_df["date"],
        rolling_sharpe,
        label=str(fund_code)
    )

plt.title(
    "Rolling 90 Day Sharpe Ratio"
)

plt.legend()

plt.savefig(
    REPORT_DIR /
    "rolling_sharpe_chart.png",
    dpi=300
)

plt.close()

# =====================================================
# COHORT ANALYSIS
# =====================================================

first_txn = (

    transactions

    .groupby(
        "investor_id"
    )

    ["transaction_date"]

    .min()

    .reset_index()

)

first_txn["cohort_year"] = (
    first_txn[
        "transaction_date"
    ]
    .dt.year
)

transactions = (
    transactions.merge(
        first_txn[
            [
                "investor_id",
                "cohort_year"
            ]
        ],
        on="investor_id"
    )
)

cohort_report = (

    transactions

    .groupby(
        "cohort_year"
    )

    .agg(

        avg_sip_amount=(
            "amount_inr",
            "mean"
        ),

        total_invested=(
            "amount_inr",
            "sum"
        )

    )

    .reset_index()

)

cohort_report.to_csv(

    PROCESSED_DIR /
    "cohort_analysis.csv",

    index=False
)

# =====================================================
# SIP CONTINUITY
# =====================================================

sip_txn = transactions[
    transactions[
        "transaction_type"
    ]
    == "Sip"
]

sip_txn = sip_txn.sort_values(
    [
        "investor_id",
        "transaction_date"
    ]
)

sip_txn["gap_days"] = (

    sip_txn

    .groupby(
        "investor_id"
    )

    ["transaction_date"]

    .diff()

    .dt.days

)

sip_continuity = (

    sip_txn

    .groupby(
        "investor_id"
    )

    .agg(

        avg_gap_days=(
            "gap_days",
            "mean"
        ),

        sip_count=(
            "transaction_date",
            "count"
        )

    )

    .reset_index()

)

sip_continuity = (
    sip_continuity[
        sip_continuity[
            "sip_count"
        ] >= 6
    ]
)

sip_continuity[
    "status"
] = np.where(

    sip_continuity[
        "avg_gap_days"
    ] > 35,

    "At Risk",

    "Healthy"
)

sip_continuity.to_csv(

    PROCESSED_DIR /
    "sip_continuity.csv",

    index=False
)

# =====================================================
# HHI
# =====================================================

hhi_report = (

    holdings

    .groupby(
        "amfi_code"
    )

    ["weight_pct"]

    .apply(

        lambda x:
        np.sum(
            (x/100)**2
        )

    )

    .reset_index()

)

hhi_report.columns = [

    "amfi_code",

    "sector_hhi"

]

hhi_report.to_csv(

    PROCESSED_DIR /
    "hhi_report.csv",

    index=False
)

insights = [

"Funds with highest VaR show greater downside risk.",

"High Sharpe funds consistently rank higher in recommendations.",

"Recent investor cohorts contribute the largest investment amounts.",

"At-risk SIP investors exhibit average payment gaps above 35 days.",

"Funds with high HHI indicate concentrated portfolios."

]

with open(

    REPORT_DIR /
    "advanced_insights.txt",

    "w",

    encoding="utf-8"

) as f:

    for item in insights:

        f.write(
            item + "\n"
        )

        # =====================================================
# FINAL SUMMARY
# =====================================================

print("=" * 60)
print("ADVANCED ANALYTICS COMPLETED")
print("=" * 60)

print(
    f"Funds Analysed : {len(risk_df)}"
)

print(
    f"Recommendations Generated : {len(recommendations)}"
)

print(
    f"Cohorts Analysed : {cohort_report.shape[0]}"
)

print(
    f"SIP Investors Analysed : {sip_continuity.shape[0]}"
)

print("\nGenerated Files:")

print("- var_cvar_report.csv")
print("- recommendations.csv")
print("- cohort_analysis.csv")
print("- sip_continuity.csv")
print("- hhi_report.csv")
print("- rolling_sharpe_chart.png")
print("- advanced_insights.txt")

logging.info(
    "Advanced Analytics Completed Successfully"
)