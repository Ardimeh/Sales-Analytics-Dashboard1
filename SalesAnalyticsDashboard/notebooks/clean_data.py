"""
clean_data.py
--------------
Cleans the raw synthetic sales dataset (data/sales_data_raw.csv) using
pandas and produces an analysis-ready CSV (data/sales_data_clean.csv).

Cleaning steps performed:
    1. Load raw data
    2. Remove exact duplicate rows
    3. Standardize text columns (trim whitespace, fix casing)
    4. Handle missing values (Customer, City, Discount)
    5. Fix invalid numeric values (negative/zero quantities)
    6. Convert data types (Date -> datetime, numeric columns -> proper dtype)
    7. Recalculate Revenue to guarantee consistency
    8. Save cleaned dataset to CSV
"""

import pandas as pd
import numpy as np

RAW_PATH = "../data/sales_data_raw.csv"
CLEAN_CSV_PATH = "../data/sales_data_clean.csv"

# ------------------------------------------------------------------
# 1. Load raw data
# ------------------------------------------------------------------
df = pd.read_csv(RAW_PATH)
print(f"Raw rows loaded: {len(df)}")

# ------------------------------------------------------------------
# 2. Remove exact duplicate rows
# ------------------------------------------------------------------
before = len(df)
df = df.drop_duplicates()
print(f"Removed {before - len(df)} exact duplicate rows")

# Also drop duplicate OrderIDs, keeping the first occurrence
# (in real data, an OrderID should be unique)
before = len(df)
df = df.drop_duplicates(subset="OrderID", keep="first")
print(f"Removed {before - len(df)} duplicate OrderIDs")

# ------------------------------------------------------------------
# 3. Standardize text columns: trim whitespace & fix casing
# ------------------------------------------------------------------
text_cols = ["Customer", "Product", "Category", "City", "Country", "Salesperson"]

for col in text_cols:
    df[col] = (
        df[col]
        .astype(str)
        .str.strip()          # remove leading/trailing whitespace
        .str.title()           # consistent Title Case
        .replace({"Nan": np.nan})  # restore true NaNs lost via astype(str)
    )

# ------------------------------------------------------------------
# 4. Handle missing values
# ------------------------------------------------------------------
# Customer: unknown customers become "Unknown Customer" rather than dropped,
# so revenue isn't lost from the analysis
df["Customer"] = df["Customer"].fillna("Unknown Customer")

# City / Country: drop rows where location is missing (small % of data,
# and geography is required for the map visuals in Power BI)
before = len(df)
df = df.dropna(subset=["City", "Country"])
print(f"Dropped {before - len(df)} rows missing City/Country")

# Discount: assume missing discount means no discount was applied
df["Discount"] = df["Discount"].fillna(0)

# ------------------------------------------------------------------
# 5. Fix invalid numeric values
# ------------------------------------------------------------------
# Negative quantities are data-entry errors -> convert to positive
df["Quantity"] = df["Quantity"].abs()

# Remove any rows where Quantity is still 0 (not a valid sale)
before = len(df)
df = df[df["Quantity"] > 0]
print(f"Dropped {before - len(df)} rows with zero quantity")

# Clip discount to a sane 0-50% range in case of outliers
df["Discount"] = df["Discount"].clip(lower=0, upper=0.5)

# ------------------------------------------------------------------
# 6. Convert data types
# ------------------------------------------------------------------
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.dropna(subset=["Date"])  # drop any unparseable dates

df["OrderID"] = df["OrderID"].astype(int)
df["Quantity"] = df["Quantity"].astype(int)
df["UnitPrice"] = df["UnitPrice"].astype(float).round(2)
df["Discount"] = df["Discount"].astype(float).round(2)

# ------------------------------------------------------------------
# 7. Recalculate Revenue to guarantee consistency with other columns
# ------------------------------------------------------------------
df["Revenue"] = (df["Quantity"] * df["UnitPrice"] * (1 - df["Discount"])).round(2)

# ------------------------------------------------------------------
# 8. Add a few helper columns useful for BI reporting
# ------------------------------------------------------------------
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["MonthName"] = df["Date"].dt.strftime("%B")
df["YearMonth"] = df["Date"].dt.strftime("%Y-%m")

# Final sort for readability
df = df.sort_values("Date").reset_index(drop=True)

print(f"\nFinal cleaned row count: {len(df)}")
print(df.dtypes)

# ------------------------------------------------------------------
# 9. Save cleaned dataset
# ------------------------------------------------------------------
df.to_csv(CLEAN_CSV_PATH, index=False)
print(f"\nCleaned data saved to: {CLEAN_CSV_PATH}")
