import pandas as pd

# Load dataset

df = pd.read_csv("data/raw/02_nav_history.csv")

# ------------------------
# 1. Parse dates
# ------------------------

df["date"] = pd.to_datetime(
    df["date"],
    errors="coerce"
)

# Invalid dates check

invalid_dates = df["date"].isna().sum()

print("Invalid dates:", invalid_dates)

# Remove invalid dates

df = df.dropna(subset=["date"])

# ------------------------
# 2. Remove duplicates
# ------------------------

duplicate_count = df.duplicated().sum()

print("Duplicate rows:", duplicate_count)

df = df.drop_duplicates()

# ------------------------
# 3. Sort values
# ------------------------

df = df.sort_values(
    by=["amfi_code", "date"]
)

# ------------------------
# 4. Forward-fill NAV
# ------------------------

df["nav"] = pd.to_numeric(
    df["nav"],
    errors="coerce"
)

df["nav"] = (
    df.groupby("amfi_code")["nav"]
      .ffill()
)

# ------------------------
# 5. Validate NAV > 0
# ------------------------

invalid_nav = (df["nav"] <= 0).sum()

print("Invalid NAV values:", invalid_nav)

# Remove invalid NAV

df = df[df["nav"] > 0]

# ------------------------
# 6. Final sort
# ------------------------

df = df.sort_values(
    by=["amfi_code", "date"]
).reset_index(drop=True)

# ------------------------
# 7. Save cleaned file
# ------------------------

output_path = "data/raw/nav_history_clean.csv"

df.to_csv(
    output_path,
    index=False
)

# ------------------------
# 8. Summary
# ------------------------

print("\nCleaning Summary")

print("------------------")

print("Final Shape:", df.shape)

print("Missing NAV:", df["nav"].isna().sum())

print("Unique Funds:", df["amfi_code"].nunique())

print("Date Range:")

print(
    df["date"].min(),
    "to",
    df["date"].max()
)

print("\nSaved:", output_path)