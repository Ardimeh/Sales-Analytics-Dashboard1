-- ============================================================
-- 02_top_10_products.sql
-- Purpose: The 10 best-selling products by total revenue.
-- Useful for: Bar chart / ranked table of top products in Power BI.
-- ============================================================

SELECT
    Product,
    Category,
    COUNT(DISTINCT OrderID)  AS TotalOrders,
    SUM(Quantity)            AS TotalUnitsSold,
    ROUND(SUM(Revenue), 2)   AS TotalRevenue
FROM sales
GROUP BY Product, Category
ORDER BY TotalRevenue DESC
LIMIT 10;
