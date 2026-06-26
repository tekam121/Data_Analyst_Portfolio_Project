import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

# ============================================================
# PostgreSQL Connection
# ============================================================

USERNAME = "postgres"
PASSWORD = quote_plus("Postgres123")   # <-- Replace with your password

HOST = "localhost"
PORT = "5432"
DATABASE = "mutual_fund"

engine = create_engine(
    f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}",
    future=True
)

# ============================================================
# CSV Folder
# ============================================================

RAW_PATH = "data/raw"

FUND_FILE = f"{RAW_PATH}/01_fund_master.csv"

NAV_FILE = f"{RAW_PATH}/nav_history_clean.csv"

TRANSACTION_FILE = f"{RAW_PATH}/investor_transactions_clean.csv"

PERFORMANCE_FILE = f"{RAW_PATH}/scheme_performance_clean.csv"

AUM_FILE = f"{RAW_PATH}/03_aum_by_fund_house.csv"

# ============================================================
# Helper Functions
# ============================================================

def print_header(title):

    print("\n" + "="*65)

    print(title)

    print("="*65)


def table_count(table_name):

    with engine.connect() as conn:

        return conn.execute(
            text(f"SELECT COUNT(*) FROM {table_name}")
        ).scalar()


def verify(table_name, csv_rows):

    db_rows = table_count(table_name)

    status = "PASS" if db_rows == csv_rows else "FAIL"

    print(f"{table_name}")

    print(f"CSV Rows : {csv_rows}")

    print(f"DB Rows  : {db_rows}")

    print(f"Status   : {status}")

    print("-"*50)


# ============================================================
# Clear Existing Data
# ============================================================

print_header("Cleaning Existing Tables")

with engine.begin() as conn:

    conn.execute(text("""
        TRUNCATE TABLE

        fact_nav,

        fact_transactions,

        fact_performance,

        fact_aum,

        dim_date,

        dim_fund

        RESTART IDENTITY

        CASCADE;
    """))

print("Existing data removed.\n")

# ============================================================
# Load Dimension Fund
# ============================================================

print_header("Loading dim_fund")

fund_df = pd.read_csv(FUND_FILE)

fund_df["launch_date"] = pd.to_datetime(
    fund_df["launch_date"],
    errors="coerce"
)

fund_df = fund_df[[
    "amfi_code",
    "fund_house",
    "scheme_name",
    "category",
    "sub_category",
    "plan",
    "launch_date",
    "benchmark",
    "expense_ratio_pct",
    "exit_load_pct",
    "min_sip_amount",
    "min_lumpsum_amount",
    "fund_manager",
    "risk_category",
    "sebi_category_code"
]]

fund_df.to_sql(

    "dim_fund",

    engine,

    if_exists="append",

    index=False,

    method="multi"

)

verify(

    "dim_fund",

    len(fund_df)

)

print("\nPart 1 Completed Successfully.")

# ============================================================
# Generate Date Dimension
# ============================================================

print_header("Generating dim_date")

date_frames = []

# NAV Dates
nav_dates = pd.read_csv(
    NAV_FILE,
    usecols=["date"]
)

nav_dates.columns = ["full_date"]

date_frames.append(nav_dates)

# Transaction Dates
txn_dates = pd.read_csv(
    TRANSACTION_FILE,
    usecols=["transaction_date"]
)

txn_dates.columns = ["full_date"]

date_frames.append(txn_dates)

# AUM Dates
aum_dates = pd.read_csv(
    AUM_FILE,
    usecols=["date"]
)

aum_dates.columns = ["full_date"]

date_frames.append(aum_dates)

# Merge all dates
dim_date = pd.concat(
    date_frames,
    ignore_index=True
)

# Convert to datetime
dim_date["full_date"] = pd.to_datetime(
    dim_date["full_date"],
    errors="coerce"
)

dim_date = dim_date.dropna()

dim_date = (
    dim_date
    .drop_duplicates()
    .sort_values("full_date")
)

# Generate Date Dimension Columns

dim_date["date_id"] = (
    dim_date["full_date"]
    .dt.strftime("%Y%m%d")
    .astype(int)
)

dim_date["year"] = dim_date["full_date"].dt.year

dim_date["quarter"] = dim_date["full_date"].dt.quarter

dim_date["month"] = dim_date["full_date"].dt.month

dim_date["month_name"] = dim_date["full_date"].dt.month_name()

dim_date["weekday"] = dim_date["full_date"].dt.weekday

dim_date["weekday_name"] = dim_date["full_date"].dt.day_name()

dim_date["is_weekday"] = (
    dim_date["weekday"] < 5
)

dim_date = dim_date[
    [
        "date_id",
        "full_date",
        "year",
        "quarter",
        "month",
        "month_name",
        "weekday",
        "weekday_name",
        "is_weekday"
    ]
]

dim_date.to_sql(

    "dim_date",

    engine,

    if_exists="append",

    index=False,

    method="multi"

)

verify(

    "dim_date",

    len(dim_date)

)

# ============================================================
# Load fact_nav
# ============================================================

print_header("Loading fact_nav")

nav_df = pd.read_csv(NAV_FILE)

nav_df["date"] = pd.to_datetime(
    nav_df["date"]
)

nav_df = nav_df.sort_values(
    [
        "amfi_code",
        "date"
    ]
)

# Calculate Daily Return %

nav_df["daily_return_pct"] = (

    nav_df

    .groupby("amfi_code")["nav"]

    .pct_change()

    *100

)

nav_df["daily_return_pct"] = (

    nav_df["daily_return_pct"]

    .fillna(0)

    .round(4)

)

# Generate date_id

nav_df["date_id"] = (

    nav_df["date"]

    .dt.strftime("%Y%m%d")

    .astype(int)

)

fact_nav = nav_df[
    [
        "amfi_code",
        "date_id",
        "nav",
        "daily_return_pct"
    ]
]

fact_nav.to_sql(

    "fact_nav",

    engine,

    if_exists="append",

    index=False,

    method="multi"

)

verify(

    "fact_nav",

    len(fact_nav)

)

print("\n✅ Part 2 Completed Successfully.")

# ============================================================
# Load fact_transactions
# ============================================================

print_header("Loading fact_transactions")

txn_df = pd.read_csv(TRANSACTION_FILE)

# Convert Transaction Date
txn_df["transaction_date"] = pd.to_datetime(
    txn_df["transaction_date"],
    errors="coerce"
)

# Generate date_id
txn_df["date_id"] = (
    txn_df["transaction_date"]
    .dt.strftime("%Y%m%d")
    .astype(int)
)

# Keep Required Columns
fact_transactions = txn_df[
    [
        "investor_id",
        "amfi_code",
        "date_id",
        "transaction_type",
        "amount_inr",
        "state",
        "city",
        "city_tier",
        "age_group",
        "gender",
        "annual_income_lakh",
        "payment_mode",
        "kyc_status"
    ]
]

fact_transactions.to_sql(

    "fact_transactions",

    engine,

    if_exists="append",

    index=False,

    method="multi"

)

verify(
    "fact_transactions",
    len(fact_transactions)
)

# ============================================================
# Load fact_performance
# ============================================================

print_header("Loading fact_performance")

performance_df = pd.read_csv(PERFORMANCE_FILE)

performance_df["anomaly_flag"] = (
    performance_df["anomaly_flag"]
    .replace({
        True: 1,
        False: 0,
        "TRUE": 1,
        "FALSE": 0,
        "True": 1,
        "False": 0
    })
    .fillna(0)
    .astype(int)
)

fact_performance = performance_df[
    [
        "amfi_code",
        "return_1yr_pct",
        "return_3yr_pct",
        "return_5yr_pct",
        "benchmark_3yr_pct",
        "alpha",
        "beta",
        "sharpe_ratio",
        "sortino_ratio",
        "std_dev_ann_pct",
        "max_drawdown_pct",
        "aum_crore",
        "expense_ratio_pct",
        "morningstar_rating",
        "risk_grade",
        "expense_ratio",
        "anomaly_flag"
    ]
]

fact_performance.to_sql(

    "fact_performance",

    engine,

    if_exists="append",

    index=False,

    method="multi"

)

verify(
    "fact_performance",
    len(fact_performance)
)

print("\n✅ Part 3 Completed Successfully.")

# ============================================================
# Load fact_aum
# ============================================================

print_header("Loading fact_aum")

aum_df = pd.read_csv(AUM_FILE)

# Convert Date
aum_df["date"] = pd.to_datetime(
    aum_df["date"],
    errors="coerce"
)

# Generate date_id
aum_df["date_id"] = (
    aum_df["date"]
    .dt.strftime("%Y%m%d")
    .astype(int)
)

# Keep Required Columns
fact_aum = aum_df[
    [
        "date_id",
        "fund_house",
        "aum_lakh_crore",
        "aum_crore",
        "num_schemes"
    ]
]

fact_aum.to_sql(

    "fact_aum",

    engine,

    if_exists="append",

    index=False,

    method="multi"

)

verify(

    "fact_aum",

    len(fact_aum)

)

# ============================================================
# FINAL DATABASE VERIFICATION
# ============================================================

print_header("FINAL DATABASE SUMMARY")

tables = [

    "dim_fund",

    "dim_date",

    "fact_nav",

    "fact_transactions",

    "fact_performance",

    "fact_aum"

]

total = 0

for table in tables:

    rows = table_count(table)

    total += rows

    print(f"{table:<25} {rows:,}")

print("\n" + "="*65)

print(f"TOTAL RECORDS LOADED : {total:,}")

print("="*65)

print("\n🎉 ETL COMPLETED SUCCESSFULLY!")

print("\nDatabase : PostgreSQL")

print("Schema   : Star Schema")

print("Status   : READY FOR SQL ANALYSIS & POWER BI")