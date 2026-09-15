SELECT
    'fact_sales' AS source,
    COUNT(*) AS line_count,
    SUM(quantity * unit_price) AS revenue
FROM fact_sales
UNION ALL
SELECT
    'sales_view' AS source,
    COUNT(*) AS line_count,
    SUM(amount) AS revenue
FROM sales;
