"""
generate_data.py
-----------------
Generates a realistic synthetic sales dataset for the Sales Analytics
Dashboard project.

Columns produced:
    OrderID, Date, Customer, Product, Category, Quantity, UnitPrice,
    Discount, Revenue, City, Country, Salesperson

The script intentionally injects a small amount of "messiness" into the
raw file (duplicate rows, missing values, inconsistent text casing,
stray whitespace) so that the cleaning step in the notebook has real
work to do -- this mirrors what beginners will encounter with real
world data.

Output:
    data/sales_data_raw.csv   (uncleaned, ~10,000+ rows including noise)
"""

import random
import numpy as np
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta

# ------------------------------------------------------------------
# 1. Setup
# ------------------------------------------------------------------
fake = Faker()
Faker.seed(42)
random.seed(42)
np.random.seed(42)

N_ROWS = 10000  # target number of clean rows before noise is injected

# ------------------------------------------------------------------
# 2. Reference / lookup data
# ------------------------------------------------------------------
# Product catalog: product -> category -> typical unit price range
PRODUCT_CATALOG = {
    "Wireless Mouse":        ("Electronics", 10, 30),
    "Mechanical Keyboard":   ("Electronics", 40, 120),
    "USB-C Charger":         ("Electronics", 15, 45),
    "Bluetooth Speaker":     ("Electronics", 25, 90),
    "4K Monitor":            ("Electronics", 150, 400),
    "Laptop Stand":          ("Office Supplies", 15, 40),
    "Office Chair":          ("Furniture", 80, 300),
    "Standing Desk":         ("Furniture", 150, 500),
    "Desk Lamp":             ("Furniture", 20, 60),
    "Notebook Set":          ("Office Supplies", 5, 15),
    "Ballpoint Pens (Box)":  ("Office Supplies", 3, 10),
    "Printer Paper (Ream)":  ("Office Supplies", 4, 12),
    "Running Shoes":         ("Apparel", 40, 130),
    "Winter Jacket":         ("Apparel", 60, 220),
    "Cotton T-Shirt":        ("Apparel", 10, 35),
    "Yoga Mat":              ("Sports & Outdoors", 15, 50),
    "Water Bottle":          ("Sports & Outdoors", 8, 25),
    "Camping Tent":          ("Sports & Outdoors", 90, 300),
    "Coffee Maker":          ("Home & Kitchen", 30, 150),
    "Blender":               ("Home & Kitchen", 25, 100),
    "Air Fryer":             ("Home & Kitchen", 50, 180),
    "Cookware Set":          ("Home & Kitchen", 60, 250),
}

PRODUCTS = list(PRODUCT_CATALOG.keys())

# City -> Country mapping so geography stays consistent
CITY_COUNTRY = {
    "New York": "United States", "Los Angeles": "United States",
    "Chicago": "United States", "Houston": "United States",
    "Toronto": "Canada", "Vancouver": "Canada",
    "London": "United Kingdom", "Manchester": "United Kingdom",
    "Berlin": "Germany", "Munich": "Germany",
    "Paris": "France", "Lyon": "France",
    "Madrid": "Spain", "Barcelona": "Spain",
    "Sydney": "Australia", "Melbourne": "Australia",
    "Mumbai": "India", "Delhi": "India",
    "Sao Paulo": "Brazil", "Rio de Janeiro": "Brazil",
    "Tokyo": "Japan", "Osaka": "Japan",
    "Dubai": "United Arab Emirates",
}
CITIES = list(CITY_COUNTRY.keys())

SALESPEOPLE = [
    "Alice Carter", "Brian Nguyen", "Carla Mendes", "David Kim",
    "Elena Petrova", "Farah Haddad", "George Okafor", "Hana Suzuki",
    "Ivan Petrov", "Julia Romano",
]

# Pre-generate a pool of customer names so the same customers reorder
CUSTOMER_POOL = [fake.name() for _ in range(1200)]

START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 12, 31)
DATE_RANGE_DAYS = (END_DATE - START_DATE).days


def random_date():
    """Return a random date between START_DATE and END_DATE, weighted
    slightly toward Nov/Dec to mimic seasonal sales spikes."""
    offset = random.randint(0, DATE_RANGE_DAYS)
    d = START_DATE + timedelta(days=offset)
    # 15% chance to nudge into Nov/Dec of the same year for seasonality
    if random.random() < 0.15:
        safe_day = min(d.day, 28)  # avoid invalid day-of-month errors
        d = d.replace(month=random.choice([11, 12]), day=safe_day)
    return d


# ------------------------------------------------------------------
# 3. Generate core rows
# ------------------------------------------------------------------
rows = []
for i in range(1, N_ROWS + 1):
    product = random.choice(PRODUCTS)
    category, low_price, high_price = PRODUCT_CATALOG[product]
    unit_price = round(random.uniform(low_price, high_price), 2)
    quantity = random.randint(1, 10)
    discount = random.choice([0, 0, 0, 0.05, 0.1, 0.15, 0.2])  # mostly 0
    city = random.choice(CITIES)
    country = CITY_COUNTRY[city]

    revenue = round(quantity * unit_price * (1 - discount), 2)

    rows.append({
        "OrderID": 100000 + i,
        "Date": random_date().strftime("%Y-%m-%d"),
        "Customer": random.choice(CUSTOMER_POOL),
        "Product": product,
        "Category": category,
        "Quantity": quantity,
        "UnitPrice": unit_price,
        "Discount": discount,
        "Revenue": revenue,
        "City": city,
        "Country": country,
        "Salesperson": random.choice(SALESPEOPLE),
    })

df = pd.DataFrame(rows)

# ------------------------------------------------------------------
# 4. Inject realistic "messiness" for the cleaning step to fix
# ------------------------------------------------------------------

# 4a. Duplicate ~1% of rows (simulating double-entry errors)
dupe_sample = df.sample(frac=0.01, random_state=1)
df = pd.concat([df, dupe_sample], ignore_index=True)

# 4b. Introduce missing values in a few columns (~2% each)
for col in ["Customer", "Discount", "City"]:
    missing_idx = df.sample(frac=0.02, random_state=2).index
    df.loc[missing_idx, col] = np.nan

# 4c. Inconsistent text casing / stray whitespace in text columns
def messy_text(x):
    if pd.isna(x):
        return x
    choice = random.random()
    if choice < 0.1:
        return f"  {x.upper()}  "
    elif choice < 0.2:
        return x.lower()
    return x

for col in ["Customer", "City", "Product", "Country", "Salesperson"]:
    df[col] = df[col].apply(messy_text)

# 4d. A few negative / zero quantities to represent data-entry errors
error_idx = df.sample(frac=0.005, random_state=3).index
df.loc[error_idx, "Quantity"] = df.loc[error_idx, "Quantity"] * -1

# 4e. Shuffle rows so duplicates aren't neatly stacked at the bottom
df = df.sample(frac=1, random_state=4).reset_index(drop=True)

# ------------------------------------------------------------------
# 5. Save raw (uncleaned) dataset
# ------------------------------------------------------------------
output_path = "sales_data_raw.csv"
df.to_csv(output_path, index=False)
print(f"Generated {len(df)} rows (including injected noise).")
print(f"Saved to: {output_path}")
print(df.head())
