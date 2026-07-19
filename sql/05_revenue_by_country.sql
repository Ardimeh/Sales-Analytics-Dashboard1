-- ============================================================
-- 05_revenue_by_country.sql
-- Purpose: Total revenue and order volume broken down by country.
-- Useful for: Map visual and country-level bar chart in Power BI.
-- ============================================================

SELECT
    Country,
    COUNT(DISTINCT OrderID)  AS TotalOrders,
    SUM(Quantity)            AS TotalUnitsSold,
    ROUND(SUM(Revenue), 2)   AS TotalRevenue,
    ROUND(AVG(Revenue), 2)   AS AvgOrderValue
FROM sales
GROUP BY Country
ORDER BY TotalRevenue DESC;
