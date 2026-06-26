-- =========================================================
-- Mutual Fund Analytics Data Warehouse
-- PostgreSQL 17 Star Schema
-- =========================================================

CREATE TABLE IF NOT EXISTS dim_fund (

    amfi_code BIGINT PRIMARY KEY,

    fund_house VARCHAR(150) NOT NULL,

    scheme_name VARCHAR(250) NOT NULL,

    category VARCHAR(100),

    sub_category VARCHAR(100),

    plan VARCHAR(30),

    launch_date DATE,

    benchmark VARCHAR(200),

    expense_ratio_pct NUMERIC(5,2),

    exit_load_pct NUMERIC(5,2),

    min_sip_amount NUMERIC(12,2),

    min_lumpsum_amount NUMERIC(12,2),

    fund_manager VARCHAR(150),

    risk_category VARCHAR(50),

    sebi_category_code VARCHAR(20)

);


CREATE TABLE IF NOT EXISTS dim_date (

    date_id INTEGER PRIMARY KEY,

    full_date DATE UNIQUE,

    year INTEGER,

    quarter INTEGER,

    month INTEGER,

    month_name VARCHAR(20),

    weekday INTEGER,

    weekday_name VARCHAR(20),

    is_weekday BOOLEAN

);


CREATE TABLE IF NOT EXISTS fact_nav (

    nav_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    amfi_code BIGINT REFERENCES dim_fund(amfi_code),

    date_id INTEGER REFERENCES dim_date(date_id),

    nav NUMERIC(12,4),

    daily_return_pct NUMERIC(8,4)

);


CREATE TABLE IF NOT EXISTS fact_transactions (

    tx_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    investor_id VARCHAR(50),

    amfi_code BIGINT REFERENCES dim_fund(amfi_code),

    date_id INTEGER REFERENCES dim_date(date_id),

    transaction_type VARCHAR(20),

    amount_inr NUMERIC(18,2),

    state VARCHAR(100),

    city VARCHAR(100),

    city_tier VARCHAR(20),

    age_group VARCHAR(30),

    gender VARCHAR(20),

    annual_income_lakh NUMERIC(10,2),

    payment_mode VARCHAR(50),

    kyc_status VARCHAR(20)

);


CREATE TABLE IF NOT EXISTS fact_performance (

    performance_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    amfi_code BIGINT REFERENCES dim_fund(amfi_code),

    return_1yr_pct NUMERIC(8,2),

    return_3yr_pct NUMERIC(8,2),

    return_5yr_pct NUMERIC(8,2),

    benchmark_3yr_pct NUMERIC(8,2),

    alpha NUMERIC(8,2),

    beta NUMERIC(8,2),

    sharpe_ratio NUMERIC(8,2),

    sortino_ratio NUMERIC(8,2),

    std_dev_ann_pct NUMERIC(8,2),

    max_drawdown_pct NUMERIC(8,2),

    aum_crore NUMERIC(18,2),

    expense_ratio_pct NUMERIC(8,2),

    morningstar_rating INTEGER,

    risk_grade VARCHAR(30),

    expense_ratio NUMERIC(8,2),

    anomaly_flag INTEGER

);


CREATE TABLE IF NOT EXISTS fact_aum (

    aum_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    date_id INTEGER REFERENCES dim_date(date_id),

    fund_house VARCHAR(150),

    aum_lakh_crore NUMERIC(18,2),

    aum_crore NUMERIC(18,2),

    num_schemes INTEGER

);