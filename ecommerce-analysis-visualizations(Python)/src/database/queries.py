# src/database/queries.py

class ECommerceQueries:
    """All your actual SQL queries organized in one place"""
    
    @staticmethod
    def customer_churn_analysis():
        return """
        -- Customer Lifetime Value Analysis
        SELECT 
            c.customer_id,
            c.first_name || ' ' || c.last_name as customer_name,
            c.province, 
            c.city,
            COUNT(o.order_id) as order_count,
            COALESCE(SUM(o.total_amount), 0) as total_spent,
            COALESCE((CURRENT_DATE - MAX(o.order_date)::date), 999) as days_since_last_purchase,
            CASE 
                WHEN MAX(o.order_date) IS NULL THEN 'New Customer'
                WHEN (CURRENT_DATE - MAX(o.order_date)::date) > 120 THEN 'High Risk'
                WHEN (CURRENT_DATE - MAX(o.order_date)::date) BETWEEN 60 AND 120 THEN 'Medium Risk'
                ELSE 'Low Risk'
            END as risk_level
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.first_name, c.last_name, c.province, c.city
        """
    
    @staticmethod
    def sales_by_province():
        return """
        -- Sales analysis by province
        SELECT 
            c.province,
            COUNT(DISTINCT o.customer_id) as customer_count,
            COUNT(o.order_id) as order_count,
            SUM(o.total_amount) as total_sales,
            AVG(o.total_amount) as avg_order_value
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.province
        ORDER BY total_sales DESC
        """
    
    @staticmethod
    def inventory_analysis():
        return """
        -- Inventory analysis
        SELECT 
            product_name,
            brand,
            stock_quantity,
            price,
            stock_quantity * cost_price as inventory_value,
            CASE 
                WHEN stock_quantity = 0 THEN 'Out of Stock'
                WHEN stock_quantity < 10 THEN 'Low Stock'
                ELSE 'Good Stock'
            END as stock_status
        FROM products
        ORDER BY stock_quantity ASC
        """
    
    @staticmethod
    def order_trends():
        return """
        -- Order trends over time
        SELECT 
            DATE(order_date) as order_date,
            COUNT(order_id) as daily_orders,
            SUM(total_amount) as daily_sales
        FROM orders 
        GROUP BY DATE(order_date)
        ORDER BY order_date
        """