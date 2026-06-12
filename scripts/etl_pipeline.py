"""
Bluestock Mutual Fund Capstone
ETL Pipeline

Author: Srinivasan S
"""

from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
import logging
from datetime import datetime
print(
    f"Execution Time : {datetime.now()}"
)
# =====================================================
# LOGGING CONFIGURATION
# =====================================================

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
print("Creating log file...")

logging.basicConfig(
    filename=LOG_DIR / "etl_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logging.info("ETL Pipeline Started")

# =====================================================
# PATH CONFIGURATION
# =====================================================

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
DB_DIR = Path("data/db")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
DB_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DB_DIR / "bluestock_mf.db"

REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def validate_dataset(df, dataset_name):
    """
    Generate basic data quality statistics.
    """

    return {
        "dataset": dataset_name,
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": int(df.isnull().sum().sum()),
        "duplicates": int(df.duplicated().sum())
    }

# =====================================================
# EXTRACT
# =====================================================

print("Loading datasets...")

fund_master = pd.read_csv(RAW_DIR / "01_fund_master.csv")
nav_history = pd.read_csv(RAW_DIR / "02_nav_history.csv")
aum = pd.read_csv(RAW_DIR / "03_aum_by_fund_house.csv")
sip = pd.read_csv(RAW_DIR / "04_monthly_sip_inflows.csv")
category = pd.read_csv(RAW_DIR / "05_category_inflows.csv")
folio = pd.read_csv(RAW_DIR / "06_industry_folio_count.csv")
performance = pd.read_csv(RAW_DIR / "07_scheme_performance.csv")
transactions = pd.read_csv(RAW_DIR / "08_investor_transactions.csv")
holdings = pd.read_csv(RAW_DIR / "09_portfolio_holdings.csv")
benchmark = pd.read_csv(RAW_DIR / "10_benchmark_indices.csv")

# =====================================================
# TRANSFORM - FUND MASTER
# =====================================================

fund_master = fund_master.drop_duplicates(subset="amfi_code")
fund_master["launch_date"] = pd.to_datetime(
    fund_master["launch_date"],
    errors="coerce"
)

# =====================================================
# TRANSFORM - NAV HISTORY
# =====================================================

nav_history["date"] = pd.to_datetime(
    nav_history["date"],
    errors="coerce"
)

nav_history["nav"] = pd.to_numeric(
    nav_history["nav"],
    errors="coerce"
)

nav_history = nav_history[nav_history["nav"] > 0]

nav_history = nav_history.sort_values(
    ["amfi_code", "date"]
)

nav_history["nav"] = (
    nav_history.groupby("amfi_code")["nav"]
    .ffill()
)

nav_history = nav_history.drop_duplicates()

master_codes = set(
    fund_master["amfi_code"]
)

nav_codes = set(
    nav_history["amfi_code"]
)

missing_codes = nav_codes - master_codes

if missing_codes:
    logging.warning(
        f"AMFI code mismatch found: {len(missing_codes)}"
    )
else:
    logging.info(
        "All NAV AMFI codes exist in fund master"
    )

# =====================================================
# TRANSFORM - AUM
# =====================================================

aum["date"] = pd.to_datetime(
    aum["date"],
    errors="coerce"
)

aum["aum_crore"] = pd.to_numeric(
    aum["aum_crore"],
    errors="coerce"
)

aum = aum[aum["aum_crore"] > 0]

# =====================================================
# TRANSFORM - SIP INFLOWS
# =====================================================

sip["month"] = pd.to_datetime(
    sip["month"],
    errors="coerce"
)

# =====================================================
# TRANSFORM - CATEGORY INFLOWS
# =====================================================

category["month"] = pd.to_datetime(
    category["month"],
    errors="coerce"
)

category["category"] = (
    category["category"]
    .astype(str)
    .str.strip()
)

# =====================================================
# TRANSFORM - FOLIO
# =====================================================

folio["month"] = pd.to_datetime(
    folio["month"],
    errors="coerce"
)

# =====================================================
# TRANSFORM - PERFORMANCE
# =====================================================

performance = performance[
    performance["expense_ratio_pct"]
    .between(0.1, 2.5)
]

performance = performance.drop_duplicates(
    subset="amfi_code"
)

# =====================================================
# TRANSFORM - TRANSACTIONS
# =====================================================

transactions["transaction_date"] = pd.to_datetime(
    transactions["transaction_date"],
    errors="coerce"
)

transactions["transaction_type"] = (
    transactions["transaction_type"]
    .astype(str)
    .str.title()
)

transactions = transactions[
    transactions["amount_inr"] > 0
]
valid_txn_types = [
    "Sip",
    "Lumpsum",
    "Redemption"
]

transactions = transactions[
    transactions["transaction_type"]
    .isin(valid_txn_types)
]
# =====================================================
# TRANSFORM - HOLDINGS
# =====================================================

holdings["portfolio_date"] = pd.to_datetime(
    holdings["portfolio_date"],
    errors="coerce"
)

holdings = holdings[
    (holdings["weight_pct"] > 0)
    & (holdings["weight_pct"] <= 100)
]

# =====================================================
# TRANSFORM - BENCHMARK
# =====================================================

benchmark["date"] = pd.to_datetime(
    benchmark["date"],
    errors="coerce"
)

benchmark["close_value"] = pd.to_numeric(
    benchmark["close_value"],
    errors="coerce"
)

# =====================================================
# LOAD CLEAN FILES
# =====================================================

print("Saving cleaned datasets...")

fund_master.to_csv(PROCESSED_DIR / "fund_master_clean.csv", index=False)
nav_history.to_csv(PROCESSED_DIR / "nav_history_clean.csv", index=False)
aum.to_csv(PROCESSED_DIR / "aum_clean.csv", index=False)
sip.to_csv(PROCESSED_DIR / "sip_clean.csv", index=False)
category.to_csv(PROCESSED_DIR / "category_clean.csv", index=False)
folio.to_csv(PROCESSED_DIR / "folio_clean.csv", index=False)
performance.to_csv(PROCESSED_DIR / "performance_clean.csv", index=False)
transactions.to_csv(PROCESSED_DIR / "transactions_clean.csv", index=False)
holdings.to_csv(PROCESSED_DIR / "holdings_clean.csv", index=False)
benchmark.to_csv(PROCESSED_DIR / "benchmark_clean.csv", index=False)

# =====================================================
# DATA QUALITY REPORT
# =====================================================

quality_report = pd.DataFrame([
    validate_dataset(fund_master, "fund_master"),
    validate_dataset(nav_history, "nav_history"),
    validate_dataset(aum, "aum_by_fund_house"),
    validate_dataset(sip, "monthly_sip_inflows"),
    validate_dataset(category, "category_inflows"),
    validate_dataset(folio, "industry_folio_count"),
    validate_dataset(performance, "scheme_performance"),
    validate_dataset(transactions, "investor_transactions"),
    validate_dataset(holdings, "portfolio_holdings"),
    validate_dataset(benchmark, "benchmark_indices")
])

quality_report.to_csv(
    REPORT_DIR / "data_quality_report.csv",
    index=False
)

logging.info(
    "Data quality report generated successfully"
)

# =====================================================
# LOAD TO SQLITE
# =====================================================

print("Loading data into SQLite...")

engine = create_engine(
    f"sqlite:///{DB_PATH}"
)

fund_master.to_sql(
    "dim_fund",
    engine,
    if_exists="replace",
    index=False
)

nav_history.to_sql(
    "fact_nav",
    engine,
    if_exists="replace",
    index=False
)

aum.to_sql(
    "fact_aum",
    engine,
    if_exists="replace",
    index=False
)

performance.to_sql(
    "fact_performance",
    engine,
    if_exists="replace",
    index=False
)

transactions.to_sql(
    "fact_transactions",
    engine,
    if_exists="replace",
    index=False
)

holdings.to_sql(
    "fact_holdings",
    engine,
    if_exists="replace",
    index=False
)

benchmark.to_sql(
    "fact_benchmark",
    engine,
    if_exists="replace",
    index=False
)

valid_kyc = [
    "Verified",
    "Pending"
]

transactions = transactions[
    transactions["kyc_status"]
    .isin(valid_kyc)
]

try:

    engine = create_engine(
        f"sqlite:///{DB_PATH}"
    )

    # all to_sql statements

    logging.info(
        "SQLite load completed"
    )

except Exception as e:

    logging.error(
        f"SQLite load failed: {e}"
    )

    raise
print("=" * 60)
print("ETL PIPELINE COMPLETED SUCCESSFULLY")
print("=" * 60)
print("Processed files saved in data/processed/")
print("SQLite database saved in data/db/bluestock_mf.db")