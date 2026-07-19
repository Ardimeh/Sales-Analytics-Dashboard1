"""
load_to_sqlite.py
-------------------
Loads the cleaned sales dataset (data/sales_data_clean.csv) into a
SQLite database (data/sales.db), ready for SQL querying and for
Power BI to connect to directly.

Table created: sales
"""

import sqlite3
import pandas as pd

CLEAN_CSV_PATH = "../data/sales_data_clean.csv"
DB_PATH = "../data/sales.db"
TABLE_NAME = "sales"

# ------------------------------------------------------------------
# 1. Load cleaned data
# ------------------------------------------------------------------
df = pd.read_csv(CLEAN_CSV_PATH, parse_dates=["Date"])
print(f"Loaded {len(df)} cleaned rows from CSV")

# ------------------------------------------------------------------
# 2. Write to SQLite
# ------------------------------------------------------------------
conn = sqlite3.connect(DB_PATH)

df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)

# ------------------------------------------------------------------
# 3. Add helpful indexes for faster querying
# ------------------------------------------------------------------
cursor = conn.cursor()
cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_date ON {TABLE_NAME}(Date)")
cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_product ON {TABLE_NAME}(Product)")
cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_customer ON {TABLE_NAME}(Customer)")
cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_country ON {TABLE_NAME}(Country)")
conn.commit()

# ------------------------------------------------------------------
# 4. Sanity check: row count in the database
# ------------------------------------------------------------------
count = cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}").fetchone()[0]
print(f"Rows loaded into SQLite table '{TABLE_NAME}': {count}")

conn.close()
print(f"Database saved to: {DB_PATH}")
