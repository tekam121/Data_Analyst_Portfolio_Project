import sqlite3
import os

DATABASE = "mutual_fund.db"
SCHEMA = "schema.sql"

# Delete old database (optional)
if os.path.exists(DATABASE):
    os.remove(DATABASE)

conn = sqlite3.connect(DATABASE)

cursor = conn.cursor()

with open(SCHEMA, "r", encoding="utf-8") as f:

    cursor.executescript(f.read())

conn.commit()

cursor.execute("""

SELECT name

FROM sqlite_master

WHERE type='table'

ORDER BY name;

""")

tables = cursor.fetchall()

print("\nDatabase Created Successfully\n")

print("Tables Created\n")

for t in tables:

    print(t[0])

conn.close()