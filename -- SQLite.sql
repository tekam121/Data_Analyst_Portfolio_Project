-- SQLite
SELECT
    f.scheme_name,
    f.fund_house,
    ROUND(MAX(fp.aum_crore),2) AS aum_crore
FROM fact_performance fp
JOIN dim_fund f
ON fp.amfi_code = f.amfi_code
GROUP BY f.scheme_name, f.fund_house
ORDER BY aum_crore DESC
LIMIT 5;