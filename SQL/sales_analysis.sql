-- ============================================================
-- Sales Performance Analytics — Analysis Queries
-- Run after Tables.sql and the insert_*.sql files.
-- All queries below were tested against the loaded dataset.
-- ============================================================

-- 1. Total sales & profit by category
SELECT p.category,
       ROUND(SUM(o.sales), 2)  AS total_sales,
       ROUND(SUM(o.profit), 2) AS total_profit
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY total_sales DESC;

-- Result: Technology > Furniture > Office Supplies by sales,
-- but Technology also leads profit by a wide margin.


-- 2. Top 5 countries by total sales
SELECT l.country,
       ROUND(SUM(o.sales), 2) AS total_sales
FROM orders o
JOIN locations l ON o.location_id = l.location_id
GROUP BY l.country
ORDER BY total_sales DESC
LIMIT 5;

-- Result: United States, Australia, France, China, Germany.


-- 3. Top 10 products by total sales
SELECT p.product_name,
       ROUND(SUM(o.sales), 2) AS total_sales
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_sales DESC
LIMIT 10;

-- Result: dominated by smartphones (Apple, Cisco, Motorola, Nokia)
-- and executive leather armchairs — matches the notebook's EDA.


-- 4. Monthly sales trend
SELECT DATE_FORMAT(o.order_date, '%Y-%m') AS year_month,
       ROUND(SUM(o.sales), 2) AS total_sales
FROM orders o
GROUP BY year_month
ORDER BY year_month;


-- 5. Average discount & profit by customer segment
SELECT c.segment,
       ROUND(AVG(o.discount), 3) AS avg_discount,
       ROUND(AVG(o.profit), 2)   AS avg_profit
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.segment;

-- Result: discount levels are similar across segments (~14%),
-- Home Office customers show slightly higher average profit.


-- 6. Running cumulative sales by month (window function)
WITH monthly AS (
    SELECT DATE_FORMAT(order_date, '%Y-%m') AS year_month,
           SUM(sales) AS monthly_sales
    FROM orders
    GROUP BY year_month
)
SELECT year_month,
       ROUND(monthly_sales, 2) AS monthly_sales,
       ROUND(SUM(monthly_sales) OVER (ORDER BY year_month), 2) AS cumulative_sales
FROM monthly
ORDER BY year_month;


-- 7. Sales rank of each product within its category (window function)
SELECT p.category,
       p.product_name,
       ROUND(SUM(o.sales), 2) AS total_sales,
       RANK() OVER (
           PARTITION BY p.category
           ORDER BY SUM(o.sales) DESC
       ) AS sales_rank_in_category
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.category, p.product_name
ORDER BY p.category, sales_rank_in_category
LIMIT 30;


-- 8. Ship mode vs. average shipping cost and order priority breakdown
SELECT s.ship_mode,
       s.order_priority,
       COUNT(*) AS order_count,
       ROUND(AVG(o.shipping_cost), 2) AS avg_shipping_cost
FROM orders o
JOIN shipping s ON o.shipping_id = s.shipping_id
GROUP BY s.ship_mode, s.order_priority
ORDER BY s.ship_mode, s.order_priority;
