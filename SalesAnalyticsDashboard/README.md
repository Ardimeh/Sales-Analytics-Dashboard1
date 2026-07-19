# 📊 Sales Analytics Dashboard

A complete, beginner-friendly data analytics project demonstrating an
end-to-end workflow: **Python (data generation & cleaning) → SQL
(analysis) → Power BI (visualization)**.

This project is designed as a portfolio piece for anyone learning data
analytics — every script is commented, every SQL query is documented,
and the folder structure follows real-world project conventions.

---

## 🎯 Project Goal

Simulate a retail company's sales data and build a full analytics
pipeline that answers key business questions:

- How is revenue trending month over month?
- Which products sell the best?
- Who are our most valuable customers?
- Which product categories drive the most revenue?
- Which countries/markets perform best?

---

## 🗂️ Project Structure

```
SalesAnalyticsDashboard/
│
├── data/
│   ├── generate_data.py          # Generates the synthetic raw dataset
│   ├── sales_data_raw.csv        # Raw, messy dataset (~10,100 rows)
│   ├── sales_data_clean.csv      # Cleaned, analysis-ready dataset
│   └── sales.db                  # SQLite database (table: sales)
│
├── sql/
│   ├── 01_monthly_sales.sql
│   ├── 02_top_10_products.sql
│   ├── 03_best_customers.sql
│   ├── 04_revenue_by_category.sql
│   └── 05_revenue_by_country.sql
│
├── notebooks/
│   ├── sales_analysis.ipynb      # Full walkthrough: clean → load → query → chart
│   ├── clean_data.py             # Standalone cleaning script
│   └── load_to_sqlite.py         # Standalone SQLite loader script
│
├── dashboard/
│   └── dashboard_recommendations.md   # Power BI build guide (KPIs, charts, slicers)
│
├── screenshots/
│   ├── monthly_sales_trend.png
│   ├── top_10_products.png
│   ├── revenue_by_category.png
│   └── revenue_by_country.png
│
└── README.md
```

---

## 🧱 Dataset Overview

A synthetic dataset of ~10,000 sales transactions (2023–2024), generated
with realistic patterns (seasonal spikes, repeat customers, varied
pricing) and intentionally-injected messiness (duplicates, missing
values, inconsistent text) so the cleaning step reflects real-world data.

| Column | Description |
|---|---|
| `OrderID` | Unique order identifier |
| `Date` | Order date |
| `Customer` | Customer name |
| `Product` | Product name |
| `Category` | Product category (Electronics, Furniture, Apparel, etc.) |
| `Quantity` | Units purchased |
| `UnitPrice` | Price per unit ($) |
| `Discount` | Discount applied (0–50%) |
| `Revenue` | Quantity × UnitPrice × (1 − Discount) |
| `City` | Customer's city |
| `Country` | Customer's country |
| `Salesperson` | Sales rep who closed the order |

---

## 🛠️ Tech Stack & Workflow

1. **Python (pandas, NumPy, Faker)** — generate a realistic raw dataset
   and clean it (remove duplicates, fix types, handle missing values,
   standardize text).
2. **SQLite** — cleaned data is loaded into a lightweight `sales.db`
   database for SQL practice and as a Power BI data source.
3. **SQL** — five analysis queries covering the core business questions
   (monthly sales, top products, best customers, revenue by category,
   revenue by country).
4. **Power BI** — dashboard build guide with recommended KPIs, charts,
   maps, slicers, and layout (see `dashboard/dashboard_recommendations.md`).

---

## ▶️ How to Reproduce This Project

```bash
# 1. Install dependencies
pip install pandas numpy faker

# 2. Generate the raw dataset
cd data
python generate_data.py

# 3. Clean the data
cd ../notebooks
python clean_data.py

# 4. Load into SQLite
python load_to_sqlite.py

# 5. (Optional) Run the full walkthrough with charts
jupyter notebook sales_analysis.ipynb
```

Then open Power BI Desktop and follow `dashboard/dashboard_recommendations.md`
to connect to `data/sales_data_clean.csv` or `data/sales.db` and build the
dashboard.

---

## 📈 Key SQL Insights (sample results from this dataset)

- **Monthly Sales** — revenue ranges roughly $130K–$165K per month, with
  a seasonal uptick in November/December.
- **Top Product** — *Standing Desk* leads with the highest total revenue,
  followed by *4K Monitor*.
- **Top Category** — *Furniture* generates the largest share of revenue
  (~27%), followed by *Electronics* (~24%).
- **Top Market** — *United States* is the largest market by revenue,
  followed closely by Canada, Japan, and Germany.

(Full results are reproducible by running the SQL files in `/sql`
against `data/sales.db`, or by re-running `notebooks/sales_analysis.ipynb`.)

---

## 🖼️ Chart Previews

See `/screenshots` for matplotlib previews of each core chart
(monthly trend, top products, category share, revenue by country) —
these mirror the visuals recommended for the Power BI dashboard.

---

## 📌 Notes for Beginners

- The `.pbix` Power BI file itself must be built in Power BI Desktop
  (it can't be generated outside of the application) — that's why this
  project provides the **data + SQL + a detailed build guide** instead
  of a pre-built file. Following `dashboard/dashboard_recommendations.md`
  step by step will get you a complete dashboard in under an hour.
- All scripts are heavily commented — read through `generate_data.py`
  and `clean_data.py` to understand common real-world data cleaning
  patterns.
- Feel free to swap in your own dataset — the SQL queries and Power BI
  guide will work as long as your table has the same column names.

---

## 📄 License

This project uses entirely synthetic, generated data and is free to use
for learning, portfolio, or teaching purposes.
