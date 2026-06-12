-- =====================================================
-- Bluestock Mutual Fund Analytics
-- Business Queries
-- =====================================================

-- =====================================================
-- 1. Total Number of Funds
-- =====================================================

SELECT COUNT(*) AS total_funds
FROM dim_fund;

-- =====================================================
-- 2. Fund Count by Category
-- =====================================================

SELECT
category,
COUNT(*) AS fund_count
FROM dim_fund
GROUP BY category
ORDER BY fund_count DESC;

-- =====================================================
-- 3. Top 10 Funds by 3-Year Return
-- =====================================================

SELECT
scheme_name,
fund_house,
return_3yr_pct
FROM fact_performance
ORDER BY return_3yr_pct DESC
LIMIT 10;

-- =====================================================
-- 4. Top 10 Funds by Sharpe Ratio
-- =====================================================

SELECT
scheme_name,
sharpe_ratio
FROM fact_performance
ORDER BY sharpe_ratio DESC
LIMIT 10;

-- =====================================================
-- 5. Top 10 Funds by Alpha
-- =====================================================

SELECT
scheme_name,
alpha
FROM fact_performance
ORDER BY alpha DESC
LIMIT 10;

-- =====================================================
-- 6. Highest AUM Fund Houses
-- =====================================================

SELECT
fund_house,
MAX(aum_crore) AS total_aum
FROM fact_aum
GROUP BY fund_house
ORDER BY total_aum DESC;

-- =====================================================
-- 7. Monthly SIP Trend
-- =====================================================

SELECT
month,
sip_inflow_crore
FROM monthly_sip_inflows
ORDER BY month;

-- =====================================================
-- 8. Category-wise Net Inflows
-- =====================================================

SELECT
category,
SUM(net_inflow_crore) AS total_inflow
FROM category_inflows
GROUP BY category
ORDER BY total_inflow DESC;

-- =====================================================
-- 9. Investor Distribution by State
-- =====================================================

SELECT
state,
COUNT(*) AS investors
FROM fact_transactions
GROUP BY state
ORDER BY investors DESC;

-- =====================================================
-- 10. Investment Amount by State
-- =====================================================

SELECT
state,
SUM(amount_inr) AS total_investment
FROM fact_transactions
GROUP BY state
ORDER BY total_investment DESC;

-- =====================================================
-- 11. Gender Distribution
-- =====================================================

SELECT
gender,
COUNT(*) AS count
FROM fact_transactions
GROUP BY gender;

-- =====================================================
-- 12. Age Group Distribution
-- =====================================================

SELECT
age_group,
COUNT(*) AS investors
FROM fact_transactions
GROUP BY age_group
ORDER BY investors DESC;

-- =====================================================
-- 13. City Tier Analysis
-- =====================================================

SELECT
city_tier,
SUM(amount_inr) AS total_amount
FROM fact_transactions
GROUP BY city_tier;

-- =====================================================
-- 14. Top Holdings Sectors
-- =====================================================

SELECT
sector,
SUM(weight_pct) AS total_weight
FROM fact_holdings
GROUP BY sector
ORDER BY total_weight DESC;

-- =====================================================
-- 15. Risk Grade Distribution
-- =====================================================

SELECT
risk_grade,
COUNT(*) AS fund_count
FROM fact_performance
GROUP BY risk_grade
ORDER BY fund_count DESC;

-- =====================================================
-- 16. Average Expense Ratio by Category
-- =====================================================

SELECT
category,
AVG(expense_ratio_pct) AS avg_expense_ratio
FROM fact_performance
GROUP BY category
ORDER BY avg_expense_ratio DESC;

-- =====================================================
-- 17. Top Funds by Morningstar Rating
-- =====================================================

SELECT
scheme_name,
morningstar_rating
FROM fact_performance
ORDER BY morningstar_rating DESC;

-- =====================================================
-- 18. Benchmark Performance
-- =====================================================

SELECT
index_name,
AVG(close_value) AS avg_index_value
FROM fact_benchmark
GROUP BY index_name;

-- =====================================================
-- 19. Transaction Volume Analysis
-- =====================================================

SELECT
transaction_type,
COUNT(*) AS txn_count,
SUM(amount_inr) AS total_amount
FROM fact_transactions
GROUP BY transaction_type;

-- =====================================================
-- 20. Top 5 Performing Funds
-- =====================================================

SELECT
scheme_name,
return_5yr_pct
FROM fact_performance
ORDER BY return_5yr_pct DESC
LIMIT 5;
