-- ============================================================
-- 04_revenue_by_category.sql
-- Purpose: Total revenue and share of business per product category.
-- Useful for: Pie / donut chart or bar chart in Power BI.
-- ============================================================

SELECT
    Category,
    COUNT(DISTINCT OrderID)  AS TotalOrders,
    SUM(Quantity)            AS TotalUnitsSold,
    ROUND(SUM(Revenue), 2)   AS TotalRevenue,
    ROUND(
        100.0 * SUM(Revenue) / (SELECT SUM(Revenue) FROM sales), 2
    )                        AS PctOfTotalRevenue
FROM sales
GROUP BY Category
ORDER BY TotalRevenue DESC;
