import pandas as pd

# Load dataset

df = pd.read_csv("data/raw/08_investor_transactions.csv")

print("Original Shape:", df.shape)

# ------------------------
# 1. Fix date format
# ------------------------

df["transaction_date"] = pd.to_datetime(
    df["transaction_date"],
    errors="coerce",
    dayfirst=True
)

invalid_dates = df["transaction_date"].isna().sum()

print("Invalid dates:", invalid_dates)

df = df.dropna(subset=["transaction_date"])

# ------------------------
# 2. Standardize transaction_type
# ------------------------

mapping = {

    "sip": "SIP",

    "systematic investment plan": "SIP",

    "monthly sip": "SIP",

    "lumpsum": "Lumpsum",

    "lump sum": "Lumpsum",

    "one time": "Lumpsum",

    "onetime": "Lumpsum",

    "redemption": "Redemption",

    "redeem": "Redemption",

    "withdrawal": "Redemption"
}

df["transaction_type"] = (

    df["transaction_type"]

      .astype(str)

      .str.strip()

      .str.lower()

      .replace(mapping)
)

valid_types = [

    "SIP",

    "Lumpsum",

    "Redemption"
]

invalid_txn = ~df["transaction_type"].isin(valid_types)

print(

    "Invalid transaction types:",

    invalid_txn.sum()

)

# Remove invalid values

df = df[~invalid_txn]

# ------------------------
# 3. Validate amount > 0
# ------------------------

df["amount_inr"] = pd.to_numeric(

    df["amount_inr"],

    errors="coerce"
)

invalid_amount = (

    (df["amount_inr"] <= 0)

    | (df["amount_inr"].isna())
)

print(

    "Invalid amount rows:",

    invalid_amount.sum()
)

df = df[~invalid_amount]

# ------------------------
# 4. Standardize KYC status
# ------------------------

kyc_mapping = {

    "yes": "Verified",

    "verified": "Verified",

    "complete": "Verified",

    "done": "Verified",

    "true": "Verified",

    "no": "Pending",

    "pending": "Pending",

    "incomplete": "Pending",

    "false": "Pending"
}

df["kyc_status"] = (

    df["kyc_status"]

      .astype(str)

      .str.strip()

      .str.lower()

      .replace(kyc_mapping)
)

valid_kyc = [

    "Verified",

    "Pending"
]

invalid_kyc = (

    ~df["kyc_status"]

      .isin(valid_kyc)
)

print(

    "Invalid KYC rows:",

    invalid_kyc.sum()
)

df = df[~invalid_kyc]

# ------------------------
# 5. Remove duplicates
# ------------------------

duplicates = df.duplicated().sum()

print(

    "Duplicate rows:",

    duplicates
)

df = df.drop_duplicates()

# ------------------------
# 6. Sort data
# ------------------------

df = df.sort_values(

    by="transaction_date"

).reset_index(drop=True)

# ------------------------
# 7. Save cleaned file
# ------------------------

output = (

    "data/raw/"

    "investor_transactions_clean.csv"
)

df.to_csv(

    output,

    index=False
)

# ------------------------
# 8. Summary
# ------------------------

print("\nCleaning Summary")

print("----------------")

print(

    "Final Shape:",

    df.shape
)

print(

    "Date Range:",

    df["transaction_date"].min(),

    "to",

    df["transaction_date"].max()
)

print(

    "Saved:",

    output
)