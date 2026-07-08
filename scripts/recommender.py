# ============================================================
# Mutual Fund Recommender System
# Bluestock Fintech Capstone Project
# ============================================================

import pandas as pd
import os

# ------------------------------------------------------------
# Load Data
# ------------------------------------------------------------

SHARPE_FILE = "C:\\Users\\tekam\\Downloads\\Data Science\\Data_Analyst_Portfolio_Project\\data\\processed\\sharpe_ratio_ranking.csv"
PERFORMANCE_FILE = "C:\\Users\\tekam\\Downloads\\Data Science\\Data_Analyst_Portfolio_Project\\data\\processed\\scheme_performance_clean.csv"

if not os.path.exists(SHARPE_FILE):
    raise FileNotFoundError(f"{SHARPE_FILE} not found")

if not os.path.exists(PERFORMANCE_FILE):
    raise FileNotFoundError(f"{PERFORMANCE_FILE} not found")

sharpe = pd.read_csv(SHARPE_FILE)
performance = pd.read_csv(PERFORMANCE_FILE)

# ------------------------------------------------------------
# Merge Data
# ------------------------------------------------------------

df = sharpe.merge(
    performance[
        [
            "scheme_name",
            "risk_grade"
        ]
    ],
    left_on="Scheme Name",
    right_on="scheme_name",
    how="left"
)

df.drop(columns=["scheme_name"], inplace=True)

# ------------------------------------------------------------
# Recommendation Function
# ------------------------------------------------------------

def recommend_funds(risk_appetite):

    risk_appetite = risk_appetite.strip().lower()

    if risk_appetite not in ["low", "moderate", "high"]:

        print("\nInvalid Risk Appetite")
        print("Choose one of these:")
        print("Low")
        print("Moderate")
        print("High")

        return

    result = (

        df[
            df["risk_grade"].str.lower() == risk_appetite
        ]

        .sort_values(
            "Sharpe Ratio",
            ascending=False
        )

        .head(3)

    )

    print("\n")
    print("=" * 70)
    print(f"Top 3 Recommended Funds ({risk_appetite.title()} Risk)")
    print("=" * 70)

    print(

        result[
            [
                "Scheme Name",
                "risk_grade",
                "Sharpe Ratio"
            ]
        ].to_string(index=False)

    )

    os.makedirs(
        "data/processed",
        exist_ok=True
    )

    result.to_csv(
        "C:\\Users\\tekam\\Downloads\\Data Science\\Data_Analyst_Portfolio_Project\\data\\processed\\fund_recommendation.csv",
        index=False
    )

    print("\nRecommendation saved successfully.")
    print("File : data/processed/fund_recommendation.csv")


# ------------------------------------------------------------
# Main Program
# ------------------------------------------------------------

if __name__ == "__main__":

    print("=" * 70)
    print("Mutual Fund Recommendation System")
    print("=" * 70)

    print("\nRisk Appetite Options")
    print("1. Low")
    print("2. Moderate")
    print("3. High")

    risk = input("\nEnter Risk Appetite : ")

    recommend_funds(risk)