-- Add indexes for better performance
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_active ON products(is_active) WHERE is_active = true;
CREATE INDEX idx_customers_province ON customers(province);
CREATE INDEX idx_order_items_product ON order_items(product_id);

-- Additional constraints for data integrity
ALTER TABLE order_items 
ADD CONSTRAINT fk_order_items_orders 
FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE;

ALTER TABLE order_items 
ADD CONSTRAINT fk_order_items_products 
FOREIGN KEY (product_id) REFERENCES products(product_id);