import pandas as pd

# Load file

df = pd.read_csv("data/raw/07_scheme_performance.csv")

print("Original Shape:", df.shape)

# ---------------------------------
# 1. Find return columns
# ---------------------------------

return_cols = [

    col for col in df.columns

    if "return" in col.lower()

]

print("\nReturn Columns:")

print(return_cols)

# ---------------------------------
# 2. Convert returns to numeric
# ---------------------------------

for col in return_cols:

    df[col] = (

        df[col]

        .astype(str)

        .str.replace("%", "", regex=False)

        .str.strip()

    )

    df[col] = pd.to_numeric(

        df[col],

        errors="coerce"

    )

# Invalid return rows

invalid_returns = (

    df[return_cols]

    .isna()

    .any(axis=1)

)

print(

    "\nInvalid Return Rows:",

    invalid_returns.sum()
)

# ---------------------------------
# 3. Flag anomalies
# ---------------------------------

anomaly_mask = pd.Series(

    False,

    index=df.index
)

for col in return_cols:

    anomaly_mask |= (

        (df[col] < -100)

        | (df[col] > 200)

    )

print(

    "Anomaly Rows:",

    anomaly_mask.sum()
)

# ---------------------------------
# 4. Expense ratio validation
# ---------------------------------

df["expense_ratio_pct"] = (

    df["expense_ratio_pct"]

      .astype(str)

      .str.replace("%", "", regex=False)

      .str.strip()
)

df["expense_ratio"] = pd.to_numeric(

    df["expense_ratio_pct"],

    errors="coerce"
)

expense_invalid = (

    (df["expense_ratio"] < 0.1)

    | (df["expense_ratio"] > 2.5)

    | (df["expense_ratio"].isna())
)

print(

    "Invalid Expense Ratio:",

    expense_invalid.sum()
)

# ---------------------------------
# 5. Remove duplicates
# ---------------------------------

duplicates = df.duplicated().sum()

print(

    "Duplicate Rows:",

    duplicates
)

df = df.drop_duplicates()

# ---------------------------------
# 6. Create anomaly flag column
# ---------------------------------

df["anomaly_flag"] = anomaly_mask

# ---------------------------------
# 7. Save cleaned data
# ---------------------------------

output = (

    "data/raw/"

    "scheme_performance_clean.csv"
)

df.to_csv(

    output,

    index=False
)

# ---------------------------------
# 8. Summary
# ---------------------------------

print("\nCleaning Summary")

print("-------------------")

print(

    "Final Shape:",

    df.shape
)

print(

    "Anomaly Rows:",

    df["anomaly_flag"].sum()
)

print(

    "Saved:",

    output
)