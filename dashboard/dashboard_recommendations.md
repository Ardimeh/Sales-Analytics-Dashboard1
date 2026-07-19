# Power BI Dashboard — Build Guide & Recommendations

This guide explains how to turn the cleaned dataset (`data/sales_data_clean.csv`
or `data/sales.db`) into a professional Power BI dashboard. It's written for
beginners — follow the sections in order.

---

## 1. Connecting Your Data

**Option A — CSV (simplest for beginners)**
1. Power BI Desktop → **Home → Get Data → Text/CSV**
2. Select `data/sales_data_clean.csv`
3. Click **Transform Data** to confirm column types (Date should import as
   a Date type, Revenue/UnitPrice/Discount as Decimal Number)
4. Click **Close & Apply**

**Option B — SQLite database**
1. Install the SQLite ODBC driver (search "SQLite ODBC driver" — free download)
2. Power BI Desktop → **Get Data → ODBC** → choose the SQLite DSN pointing
   at `data/sales.db`
3. Select the `sales` table and load

Either option produces the same single table, `sales`, to build visuals from.

---

## 2. Recommended Data Model / Calculated Columns

Power BI can compute these directly in DAX, or you can reuse the columns
already added in the notebook (`Year`, `Month`, `MonthName`, `YearMonth`).

Suggested **Measures** (Modeling → New Measure):

```DAX
Total Revenue = SUM(sales[Revenue])

Total Orders = DISTINCTCOUNT(sales[OrderID])

Total Units Sold = SUM(sales[Quantity])

Average Order Value = DIVIDE([Total Revenue], [Total Orders])

Unique Customers = DISTINCTCOUNT(sales[Customer])

Revenue MoM % Change =
VAR CurrentMonthRevenue = [Total Revenue]
VAR PreviousMonthRevenue =
    CALCULATE([Total Revenue], DATEADD(sales[Date], -1, MONTH))
RETURN DIVIDE(CurrentMonthRevenue - PreviousMonthRevenue, PreviousMonthRevenue)
```

Also build a proper **Date table** (Modeling → New Table) for time
intelligence functions like `DATEADD` to work correctly:

```DAX
DateTable = CALENDAR(MIN(sales[Date]), MAX(sales[Date]))
```
Then mark it as a Date table and relate it to `sales[Date]` (1-to-many).

---

## 3. Page Layout Recommendation

### Page 1 — Executive Overview

| Visual | Details |
|---|---|
| **KPI Cards** (top row) | Total Revenue, Total Orders, Average Order Value, Unique Customers |
| **Line Chart** | Monthly Revenue trend (X: `YearMonth`, Y: `Total Revenue`) — matches `sql/01_monthly_sales.sql` |
| **Bar Chart** | Top 10 Products by Revenue (horizontal bar, sorted descending) — matches `sql/02_top_10_products.sql` |
| **Donut Chart** | Revenue by Category — matches `sql/04_revenue_by_category.sql` |
| **Map (Filled or Bubble Map)** | Revenue by Country, sized/colored by `Total Revenue` — matches `sql/05_revenue_by_country.sql` |

### Page 2 — Customers & Salespeople

| Visual | Details |
|---|---|
| **Table/Matrix** | Best Customers ranked by Total Revenue (matches `sql/03_best_customers.sql`), columns: Customer, Total Orders, Total Units, Total Revenue, Avg Order Value |
| **Bar Chart** | Revenue by Salesperson |
| **Scatter Chart** | Customer order count (X) vs. average order value (Y), bubble size = total revenue — helps spot high-value vs. high-frequency customers |

### Page 3 — Product & Geography Deep Dive

| Visual | Details |
|---|---|
| **Treemap** | Revenue by Category → Product (drill-down) |
| **Bar Chart** | Revenue by Country (matches `sql/05_revenue_by_country.sql`) |
| **Column Chart** | Units Sold by Product, colored by Category |
| **Table** | Full detail table with conditional formatting on Revenue |

---

## 4. KPI Cards to Include

- **Total Revenue** — headline number, formatted as currency
- **Total Orders** — count of distinct OrderIDs
- **Average Order Value** — Total Revenue / Total Orders
- **Unique Customers** — distinct customer count
- **Total Units Sold** — sum of Quantity
- Optional: **Revenue MoM % Change** with a conditional-formatting arrow (▲/▼)

---

## 5. Slicers & Filters (add to every page, or a shared filter pane)

- **Date range slicer** (between slider on `Date` or `YearMonth`)
- **Category** slicer (single or multi-select buttons)
- **Country** slicer (dropdown)
- **Salesperson** slicer (dropdown or list)
- Optional: **Product** search slicer for large catalogs

Tip: Sync slicers across all report pages via **View → Sync Slicers** so
filtering carries through the whole report.

---

## 6. Formatting & Design Tips for Beginners

- Use a consistent color theme (Power BI → **View → Themes**) — pick one
  accent color for revenue/positive metrics and a neutral gray for
  secondary metrics.
- Keep KPI cards at the top of every page so key numbers are always visible.
- Use **tooltips** (custom tooltip pages) to show extra detail on hover
  without cluttering the main visual.
- Add a **title text box** and your name/date to the top of the report for
  a professional touch.
- Use **drill-through pages**: e.g. clicking a country on the map jumps to
  a detail page filtered to that country.

---

## 7. Suggested File Name

Save your Power BI file as:
`dashboard/Sales_Analytics_Dashboard.pbix`

(Power BI Desktop is required to open/edit `.pbix` files — this repo
includes the data and SQL so you can rebuild the dashboard from scratch,
since `.pbix` files can't be generated outside of Power BI Desktop itself.)

---

## 8. Chart Previews (from the Python analysis notebook)

The `screenshots/` folder contains matplotlib previews of the core charts,
generated in `notebooks/sales_analysis.ipynb`, so you can see what shape
the data takes before building the same visuals in Power BI:

- `monthly_sales_trend.png` — Monthly Revenue Trend (Line Chart)
- `top_10_products.png` — Top 10 Products by Revenue (Bar Chart)
- `revenue_by_category.png` — Revenue Share by Category (Pie/Donut Chart)
- `revenue_by_country.png` — Revenue by Country (Bar Chart / Map data)
