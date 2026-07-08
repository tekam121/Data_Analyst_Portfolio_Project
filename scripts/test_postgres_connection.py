from sqlalchemy import create_engine, text

# -----------------------------
# PostgreSQL Connection Details
# -----------------------------

USERNAME = "postgres"
PASSWORD = "Postgres123"
HOST = "localhost"
PORT = "5432"
DATABASE = "mutual_fund"

engine = create_engine(
    f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
)

try:
    with engine.connect() as conn:
        version = conn.execute(text("SELECT version();")).scalar()

    print("✅ PostgreSQL Connected Successfully!\n")
    print(version)

except Exception as e:
    print("❌ Connection Failed")
    print(e)