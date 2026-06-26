
import pandas as pd 
from sqlalchemy import create_engine, text

ENGINE = create_engine("sqlite:///mutual_fund.db")
RAW = "data/raw"

def table_count(conn, table):
    return conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()

with ENGINE.begin() as conn:
    # Clear fact tables first, then dimensions
    for t in [
        "fact_nav","fact_transactions","fact_performance","fact_aum",
        "dim_date","dim_fund"
    ]:
        conn.execute(text(f"DELETE FROM {t}"))

print("Loading dim_fund...")
fund = pd.read_csv(f"{RAW}/01_fund_master.csv")
fund["launch_date"] = pd.to_datetime(fund["launch_date"], errors="coerce")
fund.to_sql("dim_fund", ENGINE, if_exists="append", index=False)

print("Generating dim_date...")
dates = []

for f,col in [
    ("nav_history_clean.csv","date"),
    ("investor_transactions_clean.csv","transaction_date"),
    ("03_aum_by_fund_house.csv","date")
]:
    d = pd.read_csv(f"{RAW}/{f}", usecols=[col])
    d.columns=["full_date"]
    dates.append(d)

dim_date = pd.concat(dates).drop_duplicates()
dim_date["full_date"]=pd.to_datetime(dim_date["full_date"],errors="coerce")
dim_date=dim_date.dropna().sort_values("full_date")
dim_date["date_id"]=dim_date["full_date"].dt.strftime("%Y%m%d").astype(int)
dim_date["year"]=dim_date["full_date"].dt.year
dim_date["month"]=dim_date["full_date"].dt.month
dim_date["month_name"]=dim_date["full_date"].dt.month_name()
dim_date["quarter"]=dim_date["full_date"].dt.quarter
dim_date["weekday"]=dim_date["full_date"].dt.weekday
dim_date["weekday_name"]=dim_date["full_date"].dt.day_name()
dim_date["is_weekday"]=(dim_date["weekday"]<5).astype(int)
dim_date=dim_date[["date_id","full_date","year","month","month_name","quarter","weekday","weekday_name","is_weekday"]]
dim_date.to_sql("dim_date",ENGINE,if_exists="append",index=False)

print("Loading fact_nav...")
nav=pd.read_csv(f"{RAW}/nav_history_clean.csv")
nav["date"]=pd.to_datetime(nav["date"])
nav=nav.sort_values(["amfi_code","date"])
nav["daily_return_pct"]=nav.groupby("amfi_code")["nav"].pct_change().fillna(0)*100
nav["date_id"]=nav["date"].dt.strftime("%Y%m%d").astype(int)
nav[["amfi_code","date_id","nav","daily_return_pct"]].to_sql("fact_nav",ENGINE,if_exists="append",index=False)

print("Loading fact_transactions...")
txn=pd.read_csv(f"{RAW}/investor_transactions_clean.csv")
txn["transaction_date"]=pd.to_datetime(txn["transaction_date"])
txn["date_id"]=txn["transaction_date"].dt.strftime("%Y%m%d").astype(int)
txn=txn.rename(columns={"amount_inr":"amount_inr"})
txn[[
"investor_id","amfi_code","date_id","transaction_type","amount_inr",
"state","city","city_tier","age_group","gender",
"annual_income_lakh","payment_mode","kyc_status"
]].to_sql("fact_transactions",ENGINE,if_exists="append",index=False)

print("Loading fact_performance...")
perf=pd.read_csv(f"{RAW}/scheme_performance_clean.csv")
cols=[
"amfi_code","return_1yr_pct","return_3yr_pct","return_5yr_pct",
"benchmark_3yr_pct","alpha","beta","sharpe_ratio","sortino_ratio",
"std_dev_ann_pct","max_drawdown_pct","aum_crore",
"expense_ratio_pct","morningstar_rating","risk_grade",
"expense_ratio","anomaly_flag"
]
perf[cols].to_sql("fact_performance",ENGINE,if_exists="append",index=False)

print("Loading fact_aum...")
aum=pd.read_csv(f"{RAW}/03_aum_by_fund_house.csv")
aum["date"]=pd.to_datetime(aum["date"])
aum["date_id"]=aum["date"].dt.strftime("%Y%m%d").astype(int)
aum[["date_id","fund_house","aum_lakh_crore","aum_crore","num_schemes"]].to_sql(
    "fact_aum",ENGINE,if_exists="append",index=False)

with ENGINE.connect() as conn:
    print("\nVerification")
    for t in ["dim_fund","dim_date","fact_nav","fact_transactions","fact_performance","fact_aum"]:
        print(f"{t}: {table_count(conn,t)} rows")

print("\nETL completed successfully.")
