from sqlalchemy import create_engine
from sqlalchemy import text

USERNAME = "postgres"
PASSWORD = "Postgres123"     # <-- apna password
HOST = "localhost"
PORT = "5432"
DATABASE = "mutual_fund"

engine = create_engine(
    f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
)

with open("sql/postgres_schema.sql", "r", encoding="utf-8") as f:
    sql_script = f.read()

with engine.begin() as conn:
    raw = conn.connection
    cursor = raw.cursor()
    cursor.execute(sql_script)
    cursor.close()

print("✅ PostgreSQL tables created successfully.")