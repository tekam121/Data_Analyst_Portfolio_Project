-- Query 1. Top 5 Funds by AUM
SELECT
    f.scheme_name,
    p.aum_crore
FROM fact_performance p
JOIN dim_fund f
ON p.amfi_code = f.amfi_code
ORDER BY p.aum_crore DESC
LIMIT 5;

-- Query 2. average NAV per month
SELECT
    d.year,
    d.month_name,
    ROUND(AVG(n.nav),2) AS avg_nav
FROM fact_nav n
JOIN dim_date d
ON n.date_id = d.date_id
GROUP BY
    d.year,
    d.month,
    d.month_name
ORDER BY
    d.year,
    d.month;


-- Query 3. SIP Year-over-Year (YoY) Growth

SELECT
    d.year,
    SUM(t.amount_inr) AS sip_amount
FROM fact_transactions t
JOIN dim_date d
ON t.date_id = d.date_id
WHERE transaction_type = 'SIP'
GROUP BY d.year
ORDER BY d.year;

-- Query 4. Transactions by State
SELECT
    state,
    COUNT(*) AS total_transactions,
    SUM(amount_inr) AS total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_amount DESC;

--Query 5. Funds with Expense Ratio < 1%
SELECT
    scheme_name,
    fund_house,
    expense_ratio_pct
FROM dim_fund
WHERE expense_ratio_pct < 1
ORDER BY expense_ratio_pct;

--Query 6. Top 10 Funds by 5-Year Return
SELECT
    f.scheme_name,
    p.return_5yr_pct
FROM fact_performance p
JOIN dim_fund f
ON p.amfi_code = f.amfi_code
ORDER BY p.return_5yr_pct DESC
LIMIT 10;

--Query 7. Transaction Type Distribution

SELECT
    transaction_type,
    COUNT(*) AS total_transactions,
    SUM(amount_inr) AS total_amount
FROM fact_transactions
GROUP BY transaction_type
ORDER BY total_transactions DESC;

--Query 8. Fund Count by Category
SELECT
    category,
    COUNT(*) AS total_funds
FROM dim_fund
GROUP BY category
ORDER BY total_funds DESC;

--Query 9. Average Investment by City Tier

SELECT
    city_tier,
    ROUND(AVG(amount_inr),2) AS avg_investment
FROM fact_transactions
GROUP BY city_tier
ORDER BY avg_investment DESC;

--Query 10. Top Fund Houses by Number of Schemes
SELECT
    fund_house,
    COUNT(*) AS total_schemes
FROM dim_fund
GROUP BY fund_house
ORDER BY total_schemes DESC;


