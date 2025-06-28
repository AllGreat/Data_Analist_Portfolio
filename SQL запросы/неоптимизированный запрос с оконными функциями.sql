-- Задача: Найти топ-3 товара по выручке в каждой категории за последний месяц,
-- а также их долю в общей выручке категории.

SELECT 
    category_id,
    product_id,
    product_name,
    revenue,
    (revenue / SUM(revenue) OVER (PARTITION BY category_id)) * 100 AS revenue_percentage
FROM (
    SELECT 
        p.category_id,
        p.product_id,
        p.product_name,
        SUM(oi.price * oi.quantity) AS revenue,
        ROW_NUMBER() OVER (PARTITION BY p.category_id ORDER BY SUM(oi.price * oi.quantity) DESC) AS rank
    FROM 
        order_items oi
    JOIN 
        products p ON oi.product_id = p.product_id
    JOIN 
        orders o ON oi.order_id = o.order_id
    WHERE 
        o.order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH)
    GROUP BY 
        p.category_id, p.product_id, p.product_name
) ranked_products
WHERE 
    rank <= 3;
