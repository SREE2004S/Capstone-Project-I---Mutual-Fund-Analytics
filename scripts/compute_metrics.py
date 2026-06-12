"""
Bluestock Mutual Fund Capstone
Performance Metrics Analytics

Author: Srinivasan S
"""

from pathlib import Path
import pandas as pd
import numpy as np
import logging
from scipy.stats import linregress
import matplotlib.pyplot as plt

# =====================================================
# LOGGING
# =====================================================

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "compute_metrics.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logging.info("Performance Analytics Started")

# =====================================================
# PATHS
# =====================================================

PROCESSED_DIR = Path("data/processed")
REPORT_DIR = Path("reports")

REPORT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# =====================================================
# INPUT FILES
# =====================================================

NAV_FILE = (
    PROCESSED_DIR /
    "nav_history_clean.csv"
)

BENCHMARK_FILE = (
    PROCESSED_DIR /
    "benchmark_clean.csv"
)

PERFORMANCE_FILE = (
    PROCESSED_DIR /
    "performance_clean.csv"
)

FUND_MASTER_FILE = (
    PROCESSED_DIR /
    "fund_master_clean.csv"
)

# =====================================================
# LOAD DATA
# =====================================================

print("Loading datasets...")

nav = pd.read_csv(
    NAV_FILE
)

benchmark = pd.read_csv(
    BENCHMARK_FILE
)

performance = pd.read_csv(
    PERFORMANCE_FILE
)

fund_master = pd.read_csv(
    FUND_MASTER_FILE
)

nav["date"] = pd.to_datetime(
    nav["date"]
)

benchmark["date"] = pd.to_datetime(
    benchmark["date"]
)

logging.info(
    "Datasets loaded successfully"
)

# =====================================================
# DAILY RETURNS
# =====================================================

nav = nav.sort_values(
    ["amfi_code", "date"]
)

nav["daily_return"] = (
    nav.groupby("amfi_code")["nav"]
    .pct_change()
)

logging.info(
    "Daily returns calculated"
)

# =====================================================
# METRIC FUNCTIONS
# =====================================================

def calculate_cagr(df, years):

    latest_date = df["date"].max()

    start_date = (
        latest_date -
        pd.DateOffset(years=years)
    )

    period_df = df[
        df["date"] >= start_date
    ]

    if len(period_df) < 2:
        return np.nan

    start_nav = (
        period_df["nav"]
        .iloc[0]
    )

    end_nav = (
        period_df["nav"]
        .iloc[-1]
    )

    cagr = (
        (end_nav / start_nav)
        ** (1 / years)
        - 1
    ) * 100

    return round(cagr, 2)


def calculate_volatility(df):

    returns = (
        df["daily_return"]
        .dropna()
    )

    if len(returns) == 0:
        return np.nan

    volatility = (
        returns.std()
        * np.sqrt(252)
        * 100
    )

    return round(
        volatility,
        2
    )


def calculate_sharpe(
    df,
    risk_free_rate=0.065
):

    returns = (
        df["daily_return"]
        .dropna()
    )

    if len(returns) == 0:
        return np.nan

    annual_return = (
        returns.mean()
        * 252
    )

    annual_vol = (
        returns.std()
        * np.sqrt(252)
    )

    if annual_vol == 0:
        return np.nan

    sharpe = (
        annual_return -
        risk_free_rate
    ) / annual_vol

    return round(
        sharpe,
        2
    )


def calculate_sortino(
    df,
    risk_free_rate=0.065
):

    returns = (
        df["daily_return"]
        .dropna()
    )

    downside_returns = (
        returns[
            returns < 0
        ]
    )

    if len(
        downside_returns
    ) == 0:
        return np.nan

    annual_return = (
        returns.mean()
        * 252
    )

    downside_std = (
        downside_returns.std()
        * np.sqrt(252)
    )

    if downside_std == 0:
        return np.nan

    sortino = (
        annual_return -
        risk_free_rate
    ) / downside_std

    return round(
        sortino,
        2
    )


def calculate_max_drawdown(df):

    nav_series = (
        df["nav"]
    )

    running_max = (
        nav_series.cummax()
    )

    drawdown = (
        nav_series /
        running_max
    ) - 1

    return round(
        drawdown.min()
        * 100,
        2
    )

logging.info(
    "Metric functions created"
)

# =====================================================
# CALCULATE METRICS FOR ALL FUNDS
# =====================================================

print("Calculating performance metrics...")

results = []

for fund_code in nav["amfi_code"].unique():

    fund_df = nav[
        nav["amfi_code"] == fund_code
    ].copy()

    if len(fund_df) < 252:
        continue

    metrics = {

        "amfi_code":
        fund_code,

        "cagr_1yr_pct":
        calculate_cagr(
            fund_df,
            1
        ),

        "cagr_3yr_pct":
        calculate_cagr(
            fund_df,
            3
        ),

        "cagr_5yr_pct":
        calculate_cagr(
            fund_df,
            5
        ),

        "volatility_pct":
        calculate_volatility(
            fund_df
        ),

        "sharpe_ratio":
        calculate_sharpe(
            fund_df
        ),

        "sortino_ratio":
        calculate_sortino(
            fund_df
        ),

        "max_drawdown_pct":
        calculate_max_drawdown(
            fund_df
        )

    }

    results.append(
        metrics
    )

fund_metrics = pd.DataFrame(
    results
)

logging.info(
    "Performance metrics calculated"
)

print(
    f"Funds processed: {len(fund_metrics)}"
)

# =====================================================
# SAVE FUND METRICS
# =====================================================

fund_metrics.to_csv(
    PROCESSED_DIR /
    "fund_metrics.csv",
    index=False
)

logging.info(
    "fund_metrics.csv created"
)

# =====================================================
# MERGE WITH PERFORMANCE DATA
# =====================================================

scorecard = fund_metrics.merge(
    performance,
    on="amfi_code",
    how="left"
)

logging.info(
    "Merged with performance dataset"
)

# =====================================================
# FUND SCORECARD
# =====================================================

print("Generating fund scorecard...")

scorecard["return_rank"] = (
    scorecard["return_3yr_pct"]
    .rank(
        ascending=True,
        pct=True
    )
)

scorecard["sharpe_rank"] = (
    scorecard["sharpe_ratio_y"]
    .rank(
        ascending=True,
        pct=True
    )
)

scorecard["alpha_rank"] = (
    scorecard["alpha"]
    .rank(
        ascending=True,
        pct=True
    )
)

scorecard["expense_rank"] = (
    scorecard["expense_ratio_pct"]
    .rank(
        ascending=False,
        pct=True
    )
)

scorecard["drawdown_rank"] = (
    scorecard["max_drawdown_pct_y"]
    .rank(
        ascending=False,
        pct=True
    )
)

scorecard["fund_score"] = (

      scorecard["return_rank"] * 30

    + scorecard["sharpe_rank"] * 25

    + scorecard["alpha_rank"] * 20

    + scorecard["expense_rank"] * 15

    + scorecard["drawdown_rank"] * 10

)

scorecard["fund_score"] = (
    scorecard["fund_score"]
    .round(2)
)

logging.info(
    "Fund scorecard generated"
)

# =====================================================
# ALPHA BETA EXPORT
# =====================================================

alpha_beta = scorecard[
[
    "amfi_code",
    "scheme_name",
    "alpha",
    "beta"
]
]

alpha_beta.to_csv(
    PROCESSED_DIR /
    "alpha_beta.csv",
    index=False
)

logging.info(
    "alpha_beta.csv created"
)

# =====================================================
# FINAL SCORECARD EXPORT
# =====================================================

final_scorecard = scorecard[
[
    "amfi_code",
    "scheme_name",
    "fund_house",
    "category",
    "return_3yr_pct",
    "cagr_1yr_pct",
    "cagr_3yr_pct",
    "cagr_5yr_pct",
    "volatility_pct",
    "sharpe_ratio_y",
    "sortino_ratio_y",
    "alpha",
    "beta",
    "expense_ratio_pct",
    "max_drawdown_pct_y",
    "fund_score"
]
]

final_scorecard = (
    final_scorecard
    .sort_values(
        "fund_score",
        ascending=False
    )
)

final_scorecard.to_csv(
    PROCESSED_DIR /
    "fund_scorecard.csv",
    index=False
)

logging.info(
    "fund_scorecard.csv created"
)

# =====================================================
# TOP 10 FUNDS
# =====================================================

top10 = (
    final_scorecard
    .head(10)
)

print("\nTOP 10 FUNDS\n")

print(
    top10[
    [
        "scheme_name",
        "fund_score"
    ]
    ]
)

# =====================================================
# BENCHMARK ANALYSIS
# =====================================================

print("Running benchmark comparison...")

nifty100 = benchmark[
    benchmark["index_name"] == "NIFTY100"
].copy()

nifty100 = nifty100.sort_values("date")

nifty100["benchmark_return"] = (
    nifty100["close_value"]
    .pct_change()
)

logging.info(
    "NIFTY100 benchmark returns calculated"
)

# =====================================================
# TRACKING ERROR
# =====================================================

tracking_error_results = []

for fund_code in nav["amfi_code"].unique():

    fund_df = nav[
        nav["amfi_code"] == fund_code
    ].copy()

    fund_df = fund_df.sort_values("date")

    fund_df["fund_return"] = (
        fund_df["nav"]
        .pct_change()
    )

    merged = pd.merge(
        fund_df[
            ["date", "fund_return"]
        ],
        nifty100[
            ["date", "benchmark_return"]
        ],
        on="date",
        how="inner"
    )

    if len(merged) < 30:
        continue

    tracking_error = (
        (
            merged["fund_return"]
            -
            merged["benchmark_return"]
        )
        .std()
        *
        np.sqrt(252)
        *
        100
    )

    tracking_error_results.append(
        {
            "amfi_code":
            fund_code,

            "tracking_error_pct":
            round(
                tracking_error,
                2
            )
        }
    )

tracking_error_df = pd.DataFrame(
    tracking_error_results
)

logging.info(
    "Tracking error calculated"
)

# =====================================================
# MERGE TRACKING ERROR
# =====================================================

final_scorecard = (
    final_scorecard.merge(
        tracking_error_df,
        on="amfi_code",
        how="left"
    )
)

# =====================================================
# SAVE UPDATED SCORECARD
# =====================================================

final_scorecard.to_csv(
    PROCESSED_DIR /
    "fund_scorecard.csv",
    index=False
)

logging.info(
    "Updated scorecard saved"
)

# =====================================================
# BENCHMARK COMPARISON CHART
# =====================================================

top5_codes = (
    final_scorecard
    .head(5)
    ["amfi_code"]
    .tolist()
)

plt.figure(
    figsize=(12, 6)
)

for fund_code in top5_codes:

    fund_df = nav[
        nav["amfi_code"]
        == fund_code
    ].copy()

    fund_df = fund_df.sort_values(
        "date"
    )

    base_nav = (
        fund_df["nav"]
        .iloc[0]
    )

    normalized = (
        fund_df["nav"]
        / base_nav
    ) * 100

    plt.plot(
        fund_df["date"],
        normalized,
        label=str(fund_code)
    )

benchmark_base = (
    nifty100["close_value"]
    .iloc[0]
)

benchmark_normalized = (
    nifty100["close_value"]
    /
    benchmark_base
) * 100

plt.plot(
    nifty100["date"],
    benchmark_normalized,
    linewidth=3,
    label="NIFTY100"
)

plt.title(
    "Top 5 Funds vs NIFTY100"
)

plt.xlabel("Date")
plt.ylabel("Growth Index")

plt.legend()

plt.tight_layout()

plt.savefig(
    REPORT_DIR /
    "benchmark_comparison.png",
    dpi=300
)

plt.close()

logging.info(
    "Benchmark comparison chart saved"
)

# =====================================================
# EXECUTION SUMMARY
# =====================================================

print("=" * 60)
print("PERFORMANCE ANALYTICS COMPLETED")
print("=" * 60)

print(
    f"Funds Analysed : {len(final_scorecard)}"
)

print(
    "Generated Files:"
)

print(
    "- fund_metrics.csv"
)

print(
    "- alpha_beta.csv"
)

print(
    "- fund_scorecard.csv"
)

print(
    "- benchmark_comparison.png"
)

logging.info(
    "Performance Analytics Completed Successfully"
)