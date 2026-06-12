# Mutual Fund Analytics Platform

A comprehensive Mutual Fund Analytics Dashboard built using Python, SQL, and Power BI. The project analyzes mutual fund industry trends, fund performance, investor behavior, SIP growth, and market trends using multiple datasets.

Developed as part of the Bluestock Fintech Capstone Project.

## Project Structure

bluestock_mf_capstone/
├── data/
│   ├── raw/           ← original downloaded files
│   ├── processed/     ← cleaned, merged CSVs
│   └── db/            ← bluestock_mf.db (SQLite)
├── notebooks/
│   ├── 01_data_ingestion.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda_analysis.ipynb
│   ├── 04_performance_analytics.ipynb
│   └── 05_advanced_analytics.ipynb
├── scripts/
│   ├── etl_pipeline.py
│   ├── live_nav_fetch.py
│   ├── compute_metrics.py
│   └── recommender.py
├── sql/
│   ├── schema.sql
│   └── queries.sql
├── dashboard/
│   └── bluestock_mf.pbix
├── reports/
│   ├── Final_Report.pdf
│   └── Presentation.pptx
└── README.md

## Project Overview

The objective of this project is to build an end-to-end analytics platform for the Indian Mutual Fund industry.

The project includes:

- Data collection and cleaning
- ETL pipeline development
- Exploratory Data Analysis (EDA)
- Data warehouse creation
- Interactive Power BI dashboard
- Business insights and reporting

The dashboard helps analyze industry growth, fund performance, investor demographics, SIP trends, and market movements.

## Objectives

- Analyze mutual fund industry growth
- Track Assets Under Management (AUM)
- Evaluate fund performance using risk and return metrics
- Study investor demographics and transaction behavior
- Monitor SIP inflows and market trends
- Build an interactive business intelligence dashboard

## Tech Stack

### Programming
- Python

### Libraries
- Pandas
- NumPy
- Matplotlib
- Plotly

### Database
- SQLite

### Visualization
- Power BI

### Version Control
- Git
- GitHub

## Datasets Used

| Dataset | Description |
|----------|-------------|
| fund_master | Mutual fund master information |
| nav_history | Historical NAV records |
| performance | Risk and return metrics |
| holdings | Portfolio holdings |
| transactions | Investor transaction data |
| sip | SIP inflow statistics |
| aum | Industry AUM data |
| category | Category level inflows |
| benchmark | Benchmark index data |
| folio | Industry folio statistics |

## ETL Pipeline

1. Extract raw CSV datasets
2. Clean missing and duplicate records
3. Standardize column names and formats
4. Create calculated metrics
5. Load cleaned datasets into SQLite
6. Connect Power BI to SQLite database

## Dashboard Pages

## How to Open the Dashboard

### Step 1: Open Power BI Desktop

Install Microsoft Power BI Desktop if not already installed.

### Step 2: Open Dashboard File

Navigate to:

dashboard/MutualFundDashboard.pbix

Double-click the .pbix file or open it from Power BI Desktop.

### Step 3: Refresh Data

Home → Refresh

This loads the latest data from the database.

### Step 4: Explore Dashboard

Available Pages:

- Industry Overview
- Fund Performance
- Investor Analytics
- SIP & Market Trends

Use slicers and filters to interact with the dashboard.

### 1. Industry Overview

- Total AUM
- SIP Inflows
- Total Folios
- Total Schemes
- AUM Trend
- AUM by AMC

### 2. Fund Performance

- Risk vs Return Scatter Plot
- Fund Scorecard
- NAV vs Benchmark Analysis
- Fund Drill Through

### 3. Investor Analytics

- Transaction Amount by State
- SIP Amount by Age Group
- Transaction Type Distribution
- Monthly Transaction Trends

### 4. SIP & Market Trends

- SIP Inflow vs Nifty 50
- Category Inflow Heatmap
- Top Categories by Net Inflow

## Key Insights

- Industry AUM crossed ₹62 lakh crore.
- SIP inflows showed consistent growth.
- Liquid funds received the highest category inflows.
- Mid Cap and Small Cap categories delivered strong returns.
- Investor participation increased across multiple states.
- SIP activity remained resilient despite market fluctuations.

## Database Connection

The dashboard is connected to the SQLite database:

database/mutual_fund.db

If Power BI requests a data source path:

Home → Transform Data → Data Source Settings

Update the database path and click Refresh.


## How to Run

### Clone Repository

git clone <repository-url>

### Install Dependencies

pip install -r requirements.txt

### Run ETL Pipeline

python run_pipeline.py

### Open Dashboard

Open the Power BI (.pbix) file and refresh the data source.

## Future Enhancements

- Real-time market integration
- Predictive fund performance models
- Investor recommendation engine
- Automated dashboard refresh
- Cloud deployment

## Conclusion

This project successfully demonstrates an end-to-end data analytics solution for the mutual fund industry. It combines data engineering, analytics, visualization, and business intelligence to provide actionable insights for investors and fund managers.