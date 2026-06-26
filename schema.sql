PRAGMA foreign_keys = ON;

----------------------------------------------------
-- DIMENSION TABLE : FUND
----------------------------------------------------

CREATE TABLE IF NOT EXISTS dim_fund (

    amfi_code TEXT PRIMARY KEY,

    fund_house TEXT NOT NULL,

    scheme_name TEXT NOT NULL,

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

----------------------------------------------------
-- DIMENSION TABLE : DATE
----------------------------------------------------

CREATE TABLE IF NOT EXISTS dim_date (

    date_id INTEGER PRIMARY KEY,

    full_date DATE UNIQUE,

    year INTEGER,

    month INTEGER,

    month_name TEXT,

    quarter INTEGER,

    weekday INTEGER,

    weekday_name TEXT,

    is_weekday INTEGER

);

----------------------------------------------------
-- FACT NAV
----------------------------------------------------

CREATE TABLE IF NOT EXISTS fact_nav (

    nav_id INTEGER PRIMARY KEY AUTOINCREMENT,

    amfi_code TEXT NOT NULL,

    date_id INTEGER NOT NULL,

    nav REAL NOT NULL,

    daily_return_pct REAL,

    FOREIGN KEY(amfi_code)

        REFERENCES dim_fund(amfi_code),

    FOREIGN KEY(date_id)

        REFERENCES dim_date(date_id)

);

----------------------------------------------------
-- FACT TRANSACTIONS
----------------------------------------------------

CREATE TABLE IF NOT EXISTS fact_transactions (

    tx_id INTEGER PRIMARY KEY AUTOINCREMENT,

    investor_id TEXT,

    amfi_code TEXT NOT NULL,

    date_id INTEGER NOT NULL,

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

        REFERENCES dim_fund(amfi_code),

    FOREIGN KEY(date_id)

        REFERENCES dim_date(date_id)

);

----------------------------------------------------
-- FACT PERFORMANCE
----------------------------------------------------

CREATE TABLE IF NOT EXISTS fact_performance (

    performance_id INTEGER PRIMARY KEY AUTOINCREMENT,

    amfi_code TEXT NOT NULL,

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

    expense_ratio REAL,

    anomaly_flag INTEGER,

    FOREIGN KEY(amfi_code)

        REFERENCES dim_fund(amfi_code)

);

----------------------------------------------------
-- FACT AUM
----------------------------------------------------

CREATE TABLE IF NOT EXISTS fact_aum (

    aum_id INTEGER PRIMARY KEY AUTOINCREMENT,

    date_id INTEGER NOT NULL,

    fund_house TEXT,

    aum_lakh_crore REAL,

    aum_crore REAL,

    num_schemes INTEGER,

    FOREIGN KEY(date_id)

        REFERENCES dim_date(date_id)

);