-- ============================================================
-- 03_best_customers.sql
-- Purpose: Rank customers by total revenue generated, to
-- identify VIP / highest-value customers.
-- Useful for: Top-customers table or bar chart in Power BI.
-- ============================================================

SELECT
    Customer,
    COUNT(DISTINCT OrderID)   AS TotalOrders,
    SUM(Quantity)             AS TotalUnitsPurchased,
    ROUND(SUM(Revenue), 2)    AS TotalRevenue,
    ROUND(AVG(Revenue), 2)    AS AvgOrderValue
FROM sales
WHERE Customer <> 'Unknown Customer'
GROUP BY Customer
ORDER BY TotalRevenue DESC
LIMIT 20;
