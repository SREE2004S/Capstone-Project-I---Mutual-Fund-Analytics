"""
Bluestock Mutual Fund Capstone
Live NAV Fetch Script

Author: Srinivasan S

Purpose:
Fetch live NAV history from MFAPI
and save it as CSV files in data/raw
"""

from pathlib import Path
import requests
import pandas as pd
import logging

# =====================================================
# LOGGING CONFIGURATION
# =====================================================

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "live_nav_fetch.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logging.info("Live NAV Fetch Started")

# =====================================================
# PATH CONFIGURATION
# =====================================================

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

# =====================================================
# FUND LIST
# =====================================================

FUNDS = {
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_Large_Cap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841
}

# =====================================================
# FETCH NAV DATA
# =====================================================

for fund_name, scheme_code in FUNDS.items():

    try:

        logging.info(
            f"Fetching data for {fund_name}"
        )

        url = (
            f"https://api.mfapi.in/mf/"
            f"{scheme_code}"
        )

        response = requests.get(
            url,
            timeout=30
        )

        response.raise_for_status()

        json_data = response.json()

        nav_df = pd.DataFrame(
            json_data["data"]
        )

        nav_df["scheme_code"] = (
            scheme_code
        )

        nav_df["scheme_name"] = (
            fund_name
        )

        nav_df["date"] = pd.to_datetime(
            nav_df["date"],
            format="%d-%m-%Y",
            errors="coerce"
        )

        nav_df["nav"] = pd.to_numeric(
            nav_df["nav"],
            errors="coerce"
        )

        nav_df = nav_df.sort_values(
            "date"
        )

        output_file = (
            RAW_DIR /
            f"{fund_name}.csv"
        )

        nav_df.to_csv(
            output_file,
            index=False
        )

        logging.info(
            f"{fund_name} saved successfully"
        )

        print(
            f"✓ {fund_name} downloaded"
        )

    except Exception as e:

        logging.error(
            f"{fund_name} failed: {e}"
        )

        print(
            f"✗ Failed: {fund_name}"
        )

# =====================================================
# SUMMARY
# =====================================================

print("=" * 60)
print("LIVE NAV FETCH COMPLETED")
print("=" * 60)
print(
    f"Files saved in: {RAW_DIR}"
)

logging.info(
    "Live NAV Fetch Completed Successfully"
)