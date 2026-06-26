# Data Dictionary

## Project

Mutual Fund Analytics Data Warehouse

---

# Dataset 1 : Fund Master

Source File

```
01_fund_master.csv
```

| Column             | Data Type | Business Definition                |
| ------------------ | --------- | ---------------------------------- |
| amfi_code          | BIGINT    | Unique identifier assigned by AMFI |
| fund_house         | VARCHAR   | Mutual Fund Company Name           |
| scheme_name        | VARCHAR   | Mutual Fund Scheme                 |
| category           | VARCHAR   | Equity / Debt / Hybrid             |
| sub_category       | VARCHAR   | Large Cap / Mid Cap etc.           |
| plan               | VARCHAR   | Direct / Regular                   |
| launch_date        | DATE      | Scheme Launch Date                 |
| benchmark          | VARCHAR   | Benchmark Index                    |
| expense_ratio_pct  | NUMERIC   | Annual Expense Ratio (%)           |
| exit_load_pct      | NUMERIC   | Exit Load (%)                      |
| min_sip_amount     | NUMERIC   | Minimum SIP Amount                 |
| min_lumpsum_amount | NUMERIC   | Minimum Lump Sum Investment        |
| fund_manager       | VARCHAR   | Fund Manager Name                  |
| risk_category      | VARCHAR   | Risk Level                         |
| sebi_category_code | VARCHAR   | SEBI Classification                |

---

# Dataset 2 : NAV History

Source File

```
nav_history_clean.csv
```

| Column    | Data Type | Business Definition |
| --------- | --------- | ------------------- |
| amfi_code | BIGINT    | Fund Identifier     |
| date      | DATE      | NAV Date            |
| nav       | NUMERIC   | Net Asset Value     |

---

# Dataset 3 : Investor Transactions

Source File

```
investor_transactions_clean.csv
```

| Column             | Data Type | Business Definition        |
| ------------------ | --------- | -------------------------- |
| investor_id        | VARCHAR   | Unique Investor ID         |
| transaction_date   | DATE      | Transaction Date           |
| amfi_code          | BIGINT    | Fund Identifier            |
| transaction_type   | VARCHAR   | SIP / Lumpsum / Redemption |
| amount_inr         | NUMERIC   | Transaction Amount         |
| state              | VARCHAR   | Investor State             |
| city               | VARCHAR   | Investor City              |
| city_tier          | VARCHAR   | Tier 1 / Tier 2 / Tier 3   |
| age_group          | VARCHAR   | Investor Age Group         |
| gender             | VARCHAR   | Investor Gender            |
| annual_income_lakh | NUMERIC   | Annual Income              |
| payment_mode       | VARCHAR   | UPI / NetBanking / Cheque  |
| kyc_status         | VARCHAR   | KYC Verification Status    |

---

# Dataset 4 : Scheme Performance

Source File

```
scheme_performance_clean.csv
```

| Column             | Data Type | Business Definition       |
| ------------------ | --------- | ------------------------- |
| amfi_code          | BIGINT    | Fund Identifier           |
| return_1yr_pct     | NUMERIC   | 1 Year Return             |
| return_3yr_pct     | NUMERIC   | 3 Year Return             |
| return_5yr_pct     | NUMERIC   | 5 Year Return             |
| benchmark_3yr_pct  | NUMERIC   | Benchmark Return          |
| alpha              | NUMERIC   | Alpha Measure             |
| beta               | NUMERIC   | Beta Measure              |
| sharpe_ratio       | NUMERIC   | Sharpe Ratio              |
| sortino_ratio      | NUMERIC   | Sortino Ratio             |
| std_dev_ann_pct    | NUMERIC   | Annual Standard Deviation |
| max_drawdown_pct   | NUMERIC   | Maximum Drawdown          |
| aum_crore          | NUMERIC   | Assets Under Management   |
| expense_ratio_pct  | NUMERIC   | Expense Ratio             |
| morningstar_rating | INTEGER   | Morningstar Rating        |
| risk_grade         | VARCHAR   | Risk Grade                |
| expense_ratio      | NUMERIC   | Expense Ratio             |
| anomaly_flag       | BOOLEAN   | Data Quality Flag         |

---

# Dataset 5 : AUM History

Source File

```
03_aum_by_fund_house.csv
```

| Column         | Data Type | Business Definition |
| -------------- | --------- | ------------------- |
| date           | DATE      | Reporting Date      |
| fund_house     | VARCHAR   | Mutual Fund House   |
| aum_lakh_crore | NUMERIC   | AUM in Lakh Crore   |
| aum_crore      | NUMERIC   | AUM in Crore        |
| num_schemes    | INTEGER   | Number of Schemes   |

---

# Database

PostgreSQL 17

---

# Star Schema

Dimension Tables

* dim_fund

* dim_date

Fact Tables

* fact_nav

* fact_transactions

* fact_performance

* fact_aum

---

# Data Source

AMFI India

MFAPI

Synthetic Investor Dataset

Project Generated Dataset
