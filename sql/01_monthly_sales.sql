-- ============================================================
-- 01_monthly_sales.sql
-- Purpose: Total revenue, order count, and units sold per month.
-- Useful for: Line chart of sales trend over time in Power BI.
-- ============================================================

SELECT
    YearMonth,                              -- e.g. '2023-01'
    COUNT(DISTINCT OrderID)  AS TotalOrders,
    SUM(Quantity)            AS TotalUnitsSold,
    ROUND(SUM(Revenue), 2)   AS TotalRevenue,
    ROUND(AVG(Revenue), 2)   AS AvgOrderRevenue
FROM sales
GROUP BY YearMonth
ORDER BY YearMonth;
