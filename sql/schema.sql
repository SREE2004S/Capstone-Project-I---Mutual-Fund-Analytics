-- =====================================================
-- Bluestock Mutual Fund Analytics
-- Database Schema
-- =====================================================

DROP TABLE IF EXISTS dim_fund;

CREATE TABLE dim_fund (
amfi_code INTEGER PRIMARY KEY,
fund_house TEXT,
scheme_name TEXT,
category TEXT,
sub_category TEXT,
plan TEXT,
launch_date DATE,
benchmark TEXT,
expense_ratio_pct REAL,
exit_load_pct REAL,
min_sip_amount REAL,
min_lumpsum_amount REAL,
fund_manager TEXT,
risk_category TEXT,
sebi_category_code TEXT
);

-- =====================================================

CREATE TABLE dim_date (
    date_id INTEGER PRIMARY KEY,
    full_date DATE,
    year INTEGER,
    quarter INTEGER,
    month INTEGER,
    month_name TEXT,
    day INTEGER,
    weekday_name TEXT
);
-- =====================================================

DROP TABLE IF EXISTS fact_nav;

CREATE TABLE fact_nav (
amfi_code INTEGER,
date DATE,
nav REAL,
FOREIGN KEY(amfi_code)
REFERENCES dim_fund(amfi_code)
);

-- =====================================================

DROP TABLE IF EXISTS fact_aum;

CREATE TABLE fact_aum (
date DATE,
fund_house TEXT,
aum_lakh_crore REAL,
aum_crore REAL,
num_schemes INTEGER
);

-- =====================================================

DROP TABLE IF EXISTS fact_performance;

CREATE TABLE fact_performance (
amfi_code INTEGER,
scheme_name TEXT,
fund_house TEXT,
category TEXT,
plan TEXT,
return_1yr_pct REAL,
return_3yr_pct REAL,
return_5yr_pct REAL,
benchmark_3yr_pct REAL,
alpha REAL,
beta REAL,
sharpe_ratio REAL,
sortino_ratio REAL,
std_dev_ann_pct REAL,
max_drawdown_pct REAL,
aum_crore REAL,
expense_ratio_pct REAL,
morningstar_rating INTEGER,
risk_grade TEXT,
FOREIGN KEY(amfi_code)
REFERENCES dim_fund(amfi_code)
);

-- =====================================================

DROP TABLE IF EXISTS fact_transactions;

CREATE TABLE fact_transactions (
investor_id INTEGER,
transaction_date DATE,
amfi_code INTEGER,
transaction_type TEXT,
amount_inr REAL,
state TEXT,
city TEXT,
city_tier TEXT,
age_group TEXT,
gender TEXT,
annual_income_lakh REAL,
payment_mode TEXT,
kyc_status TEXT,
FOREIGN KEY(amfi_code)
REFERENCES dim_fund(amfi_code)
);

-- =====================================================

DROP TABLE IF EXISTS fact_holdings;

CREATE TABLE fact_holdings (
amfi_code INTEGER,
stock_symbol TEXT,
stock_name TEXT,
sector TEXT,
weight_pct REAL,
market_value_cr REAL,
current_price_inr REAL,
portfolio_date DATE,
FOREIGN KEY(amfi_code)
REFERENCES dim_fund(amfi_code)
);

-- =====================================================

DROP TABLE IF EXISTS fact_benchmark;

CREATE TABLE fact_benchmark (
date DATE,
index_name TEXT,
close_value REAL
);
