"""
==============================================================
Mutual Fund Analytics Platform
Master Pipeline Runner

Author : Kamlesh Tekam

Description:
Runs the complete ETL pipeline and utility scripts
for the Mutual Fund Analytics Platform.

Execution Order:
1. Data Ingestion
2. Live NAV Fetch
3. Clean NAV Data
4. Clean Investor Transactions
5. Clean Scheme Performance
6. Create PostgreSQL Tables
7. Load Data into PostgreSQL
8. Test PostgreSQL Connection
9. Fund Recommender

Run:
    python run_pipeline.py
==============================================================
"""

import subprocess
import sys
import os

# -------------------------------------------------------------
# List of scripts in execution order
# -------------------------------------------------------------

SCRIPTS = [
    "data_ingestion.py",
    "live_nav_fetch.py",
    "clean_nav.py",
    "clean_investor_transactions.py",
    "clean_scheme_performance.py",
    "create_tables.py",
    "load_to_postgres.py",
    "test_postgres_connection.py",
    "recommender.py"
]


def run_script(script_name):
    """
    Executes a Python script.

    Parameters
    ----------
    script_name : str
        Name of the Python script to execute.
    """

    print("\n" + "=" * 70)
    print(f"Running : {script_name}")
    print("=" * 70)

    if not os.path.exists(script_name):
        print(f"❌ File not found : {script_name}")
        return False

    try:
        subprocess.run(
            [sys.executable, script_name],
            check=True
        )

        print(f"✅ Completed : {script_name}")
        return True

    except subprocess.CalledProcessError:

        print(f"❌ Error while executing : {script_name}")
        return False


def main():
    """
    Main Pipeline
    """
    risk = "Moderate"

    recommend_funds(risk)

    print("\n")
    print("=" * 70)
    print("Mutual Fund Analytics Platform")
    print("Master Pipeline Execution Started")
    print("=" * 70)

    success = 0

    for script in SCRIPTS:

        status = run_script(script)

        if status:
            success += 1
        else:
            print("\nPipeline Stopped.")
            return

    print("\n")
    print("=" * 70)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 70)

    print(f"Scripts Executed : {success}/{len(SCRIPTS)}")

    print("\nNext Steps")
    print("- Open notebooks/EDA_Analysis.ipynb")
    print("- Open notebooks/Performance_Analytics.ipynb")
    print("- Open notebooks/Advanced_Analytics.ipynb")
    print("- Open Power BI Dashboard (.pbix)")
    print("=" * 70)


if __name__ == "__main__":
    main()
