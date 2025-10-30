-- Customer Lifetime Value Analysis
-- تحلیل  ریسک ترک مشتریان
SELECT 
    c.customer_id as "کد مشتری",
    c.first_name || ' ' || c.last_name as "نام مشتری",
    c.province as "استان", 
    c.city as "شهر",
    
    -- آمار خرید
    COUNT(o.order_id) as "تعداد سفارشات",
    TO_CHAR(COALESCE(SUM(o.total_amount), 0), '999,999,999') as "مجموع خرید",
    
    -- تحلیل زمانی
    CASE 
        WHEN MAX(o.order_date) IS NULL THEN '❌ بدون سابقه خرید'
        ELSE TO_CHAR(MAX(o.order_date), 'YYYY-MM-DD')
    END as "تاریخ آخرین خرید",
    
    -- روز از آخرین خرید
    COALESCE((CURRENT_DATE - MAX(o.order_date)::date), 999) as "روز از آخرین خرید",
    
    -- سطح ریسک ترک (با معیارهای واقعی)
    CASE 
        WHEN MAX(o.order_date) IS NULL THEN '🔴 مشتری جدید - بدون خرید'
        WHEN (CURRENT_DATE - MAX(o.order_date)::date) > 120 THEN '🔴 ریسک بسیار بالا'
        WHEN (CURRENT_DATE - MAX(o.order_date)::date) BETWEEN 90 AND 120 THEN '🔴 ریسک بالا'
        WHEN (CURRENT_DATE - MAX(o.order_date)::date) BETWEEN 60 AND 90 THEN '🟡 ریسک متوسط'
        WHEN (CURRENT_DATE - MAX(o.order_date)::date) BETWEEN 30 AND 60 THEN '🔵 نیاز توجه'
        WHEN (CURRENT_DATE - MAX(o.order_date)::date) BETWEEN 7 AND 30 THEN '🟢 فعال اخیر'
        ELSE '🟢 بسیار فعال'
    END as "وضعیت مشتری",
    
    -- ارزش مشتری
    CASE 
        WHEN COALESCE(SUM(o.total_amount), 0) > 20000000 THEN '💎 با ارزش بسیار بالا'
        WHEN COALESCE(SUM(o.total_amount), 0) > 10000000 THEN '⭐ با ارزش بالا' 
        WHEN COALESCE(SUM(o.total_amount), 0) > 5000000 THEN '📊 ارزش متوسط'
        ELSE '📈 ارزش پایین'
    END as "سطح ارزش",
   
    -- اقدامات پیشنهادی برای تیم فروش
    CASE 
        WHEN MAX(o.order_date) IS NULL THEN 'ارسال کد تخفیف ۲۰٪ برای اولین خرید'
        WHEN (CURRENT_DATE - MAX(o.order_date)::date) > 120 THEN 'تماس فوری + پیشنهاد ۵۰٪ تخفیف + هدیه'
        WHEN (CURRENT_DATE - MAX(o.order_date)::date) BETWEEN 90 AND 120 THEN 'تماس مستقیم + پیشنهاد ۴۰٪ تخفیف'
        WHEN (CURRENT_DATE - MAX(o.order_date)::date) BETWEEN 60 AND 90 THEN 'ایمیل شخصی + نظرسنجی رضایت'
        WHEN (CURRENT_DATE - MAX(o.order_date)::date) BETWEEN 30 AND 60 THEN 'خبرنامه محصولات جدید + نظرسنجی'
        ELSE 'برنامه وفاداری + پیشنهادات ویژه'
    END as "اقدام بازاریابی"

FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.province, c.city
ORDER BY 
    CASE 
        WHEN MAX(o.order_date) IS NULL THEN 1
        WHEN (CURRENT_DATE - MAX(o.order_date)::date) > 120 THEN 2
        WHEN (CURRENT_DATE - MAX(o.order_date)::date) BETWEEN 90 AND 120 THEN 3
        WHEN (CURRENT_DATE - MAX(o.order_date)::date) BETWEEN 60 AND 90 THEN 4
        ELSE 5
    END,
    "روز از آخرین خرید" DESC;

-- 5. Predictive Analytics: Customer Churn Risk
-- APPROACH 1: Single Query (Clean & Efficient)
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name as customer_name,
    c.province,
    (CURRENT_DATE - MAX(o.order_date)::date) as days_since_last_purchase,
    COUNT(o.order_id) as total_orders,
    SUM(o.total_amount) as total_spent,
    CASE 
        WHEN (CURRENT_DATE - MAX(o.order_date)::date) > 90 THEN 'High Risk - Churned'
        WHEN (CURRENT_DATE - MAX(o.order_date)::date) BETWEEN 60 AND 90 THEN 'Medium Risk'
        ELSE 'Low Risk - Active'
    END as churn_risk
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.province;

-- APPROACH 2: Subquery (More Readable for Complex Logic)
SELECT 
    customer_id,
    customer_name,
    province,
    (CURRENT_DATE - last_purchase_date) as days_since_last_purchase,
    total_orders,
    total_spent,
    CASE 
        WHEN (CURRENT_DATE - last_purchase_date) > 90 THEN 'High Risk - Churned'
        WHEN (CURRENT_DATE - last_purchase_date) BETWEEN 60 AND 90 THEN 'Medium Risk'
        ELSE 'Low Risk - Active'
    END as churn_risk
FROM (
    SELECT 
        c.customer_id, 
        c.first_name || ' ' || c.last_name as customer_name,
        c.province,
        MAX(o.order_date) as last_purchase_date,
        COUNT(o.order_id) as total_orders,
        SUM(o.total_amount) as total_spent
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.first_name, c.last_name, c.province
) customer_stats;

-- تحلیل ریسک ترک مشتریان با معیارهای کسب‌وکار ایرانی
SELECT 
    customer_id,
    first_name || ' ' || last_name as "نام مشتری",
    province as "استان",
    city as "شهر",
    COALESCE((CURRENT_DATE - last_purchase_date::date), 999) as "روز از آخرین خرید",
    COALESCE(order_count, 0) as "تعداد سفارشات",
    COALESCE(TO_CHAR(total_spent, '999,999,999'), '۰') as "مجموع خرید (تومان)",
    CASE 
        WHEN last_purchase_date IS NULL THEN '❌ هرگز خرید نکرده'
        WHEN (CURRENT_DATE - last_purchase_date::date) > 120 THEN '🔴 ریسک بسیار بالا'
        WHEN (CURRENT_DATE - last_purchase_date::date) BETWEEN 90 AND 120 THEN '🟠 ریسک بالا'
        WHEN (CURRENT_DATE - last_purchase_date::date) BETWEEN 60 AND 90 THEN '🟡 نیاز توجه'
        WHEN (CURRENT_DATE - last_purchase_date::date) BETWEEN 30 AND 60 THEN '🔵 فعال معمولی'
        ELSE '🟢 بسیار فعال'
    END as "وضعیت مشتری",
    
    -- توصیه‌های عملی برای تیم فروش
    CASE 
        WHEN last_purchase_date IS NULL THEN 'ارسال کد تخفیف اولین خرید'
        WHEN (CURRENT_DATE - last_purchase_date::date) > 90 THEN 'تماس مستقیم و پیشنهاد ویژه'
        WHEN (CURRENT_DATE - last_purchase_date::date) BETWEEN 60 AND 90 THEN 'ایمیل شخصی‌سازی شده'
        ELSE 'ارسال خبرنامه معمولی'
    END as "اقدام پیشنهادی"

FROM (
    SELECT 
        c.customer_id, c.first_name, c.last_name, c.province, c.city,
        MAX(o.order_date) as last_purchase_date,
        COUNT(o.order_id) as order_count,
        SUM(o.total_amount) as total_spent
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.first_name, c.last_name, c.province, c.city
) customer_analysis
ORDER BY 
    CASE 
        WHEN last_purchase_date IS NULL THEN 1
        WHEN (CURRENT_DATE - last_purchase_date::date) > 90 THEN 2
        ELSE 3
    END,
    total_spent DESC NULLS LAST;

-- تحلیل فرصت بازیابی مشتریان
SELECT 
    'فرصت بازیابی درآمد' as "تحلیل",
    TO_CHAR(SUM(total_spent) * 0.3, '999,999,999') as "درآمد قابل بازیابی (تومان)",
    'با ۳۰٪ نرخ موفقیت' as "فرضیه",
    'برنامه تماس فوری + تخفیف ویژه' as "راهکار"
FROM (
    SELECT 
        c.customer_id,
        SUM(o.total_amount) as total_spent,
        MAX(o.order_date) as last_purchase_date
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id
    HAVING (CURRENT_DATE - MAX(o.order_date)::date) > 120  -- FIX: HAVING instead of WHERE
) high_risk_customers;

-- خلاصه اجرایی برای مدیریت
SELECT 
    'مشتریان در معرض ترک' as "عنوان",
    COUNT(*) as "تعداد مشتریان",
    TO_CHAR(SUM(total_spent), '999,999,999') as "ارزش کل در خطر",
    'فوری - نیاز به اقدام سریع' as "اولویت"
FROM (
    SELECT 
        c.customer_id,
        SUM(o.total_amount) as total_spent,
        MAX(o.order_date) as last_purchase_date
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id
    HAVING (CURRENT_DATE - MAX(o.order_date)::date) > 120  -- FIX: HAVING instead of WHERE
) high_risk_customers;


SELECT 
    'تحلیل ریسک کلی کسب‌وکار' as "بخش",
    COUNT(DISTINCT customer_id) as "کل مشتریان",  -- FIX: Removed "c."
    SUM(CASE WHEN days_since_last_purchase > 120 THEN 1 ELSE 0 END) as "مشتریان پرریسک",
    ROUND(SUM(CASE WHEN days_since_last_purchase > 120 THEN 1 ELSE 0 END) * 100.0 / COUNT(DISTINCT customer_id), 1) as "درصد مشتریان پرریسک",  -- FIX: Removed "c."
    TO_CHAR(SUM(total_spent), '999,999,999') as "کل درآمد تاریخی",
    TO_CHAR(SUM(CASE WHEN days_since_last_purchase > 120 THEN total_spent ELSE 0 END), '999,999,999') as "درآمد در معرض خطر",
    ROUND(SUM(CASE WHEN days_since_last_purchase > 120 THEN total_spent ELSE 0 END) * 100.0 / SUM(total_spent), 1) as "درصد درآمد در خطر"
FROM (
    SELECT 
        c.customer_id,
        SUM(o.total_amount) as total_spent,
        (CURRENT_DATE - MAX(o.order_date)::date) as days_since_last_purchase
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id
) customer_metrics;

