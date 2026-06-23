import pandas as pd

fund_master = pd.read_csv("data/raw/01_fund_master.csv")

nav_history = pd.read_csv("data/raw/02_nav_history.csv")

print("Fund Master Shape:", fund_master.shape)

print("NAV History Shape:", nav_history.shape)

print("\nFund Master Columns")

print(fund_master.columns)

print("\nNAV History Columns")

print(nav_history.columns)

fund_codes = set(fund_master["amfi_code"])

nav_codes = set(nav_history["amfi_code"])

missing_codes = fund_codes - nav_codes

print("\nMissing AMFI Codes")

print(missing_codes)

print("\nTotal Missing")

print(len(missing_codes))