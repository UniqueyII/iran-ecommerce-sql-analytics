SELECT 
    order_id, 
    order_date, 
    (CURRENT_DATE - order_date::date) as days_ago,
    CASE 
        WHEN (CURRENT_DATE - order_date::date) > 120 THEN 'HIGH RISK'
        WHEN (CURRENT_DATE - order_date::date) BETWEEN 60 AND 120 THEN 'MEDIUM RISK'
        ELSE 'LOW RISK'
    END as risk_level
FROM orders 
ORDER BY days_ago DESC;

-- 1. تحلیل فروش به تفکیک استان
SELECT 
    c.province as "استان",
    COUNT(DISTINCT o.customer_id) as "تعداد مشتریان",
    COUNT(o.order_id) as "تعداد سفارشات",
    TO_CHAR(SUM(o.total_amount), '999,999,999') as "مجموع فروش (تومان)",
    TO_CHAR(AVG(o.total_amount), '999,999,999') as "میانگین سبد خرید"
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.province
ORDER BY SUM(o.total_amount) DESC;

-- 2. موجودی و ارزش ریالی انبار
SELECT 
    p.product_name as "نام محصول",
    p.brand as "برند",
    p.stock_quantity as "موجودی",
    TO_CHAR(p.price, '999,999,999') as "قیمت فروش",
    TO_CHAR(p.stock_quantity * p.cost_price, '999,999,999') as "ارزش موجودی (تومان)",
    CASE 
        WHEN p.stock_quantity = 0 THEN '🟥 اتمام موجودی'
        WHEN p.stock_quantity < 10 THEN '🟨 موجودی کم'
        ELSE '🟩 موجودی کافی'
    END as "وضعیت موجودی"
FROM products p
ORDER BY p.stock_quantity ASC;

-- 3. مشتریان وفادار (بر اساس تعداد و ارزش خرید)
SELECT 
    c.first_name || ' ' || c.last_name as "نام مشتری",
    c.province || ' - ' || c.city as "شهرستان",
    COUNT(o.order_id) as "تعداد سفارشات",
    TO_CHAR(SUM(o.total_amount), '999,999,999') as "مجموع خرید (تومان)",
    TO_CHAR(AVG(o.total_amount), '999,999,999') as "میانگین سبد خرید",
    CASE 
        WHEN COUNT(o.order_id) >= 3 THEN 'مشتری طلایی'
        WHEN COUNT(o.order_id) = 2 THEN 'مشتری نقرهای'
        ELSE 'مشتری جدید'
    END as "سطح وفاداری"
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.province, c.city
HAVING COUNT(o.order_id) > 0
ORDER BY SUM(o.total_amount) DESC;
