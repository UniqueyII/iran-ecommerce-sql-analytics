BEGIN;

DELETE FROM order_items;
DELETE FROM orders;
DELETE FROM products;
DELETE FROM customers;
DELETE FROM categories;

ALTER SEQUENCE categories_category_id_seq RESTART WITH 1;
ALTER SEQUENCE customers_customer_id_seq RESTART WITH 1;
ALTER SEQUENCE products_product_id_seq RESTART WITH 1;
ALTER SEQUENCE orders_order_id_seq RESTART WITH 1;
ALTER SEQUENCE order_items_order_item_id_seq RESTART WITH 1;

-- Insert categories
INSERT INTO categories (category_id, category_name, parent_category_id, description) VALUES
(1, 'الکترونیک', NULL, 'کالاهای الکترونیکی'),
(2, 'خانه و آشپزخانه', NULL, 'لوازم خانه و آشپزخانه'),
(3, 'مد و پوشاک', NULL, 'لباس و پوشاک')
ON CONFLICT (category_id) DO NOTHING;

-- Insert sub-categories
INSERT INTO categories (category_id, category_name, parent_category_id, description) VALUES
(4, 'موبایل و تبلت', 1, 'گوشی موبایل و تبلت'),
(5, 'لپ تاپ و کامپیوتر', 1, 'لپ تاپ و تجهیزات کامپیوتر'),
(6, 'لوازم جانبی', 1, 'لوازم جانبی الکترونیکی')
ON CONFLICT (category_id) DO NOTHING;

-- Insert customers
INSERT INTO customers (national_code, first_name, last_name, province, city, phone, email, birth_date) VALUES
('0123456769', 'علی', 'محمدی', 'تهران', 'تهران', '09121234667', 'ali.mohamadi@email.com', '1990-05-15'),
('1234567890', 'فاطمه', 'احمدی', 'اصفهان', 'اصفهان', '09123456789', 'fateme.ahmadi@email.com', '1992-08-22'),
('2345678901', 'محمد', 'کریمی', 'خراسان رضوی', 'مشهد', '09134567890', 'mohammad.karimi@email.com', '1988-12-10'),
('3456789012', 'زهرا', 'حسینی', 'آذربایجان شرقی', 'تبریز', '09145678901', 'zahra.hosseini@email.com', '1995-03-30'),
('4567890123', 'رضا', 'جعفری', 'فارس', 'شیراز', '09156789012', 'reza.jafari@email.com', '1993-07-18')
ON CONFLICT (national_code) DO NOTHING;

-- Insert products (FIXED category_id references)
INSERT INTO products (product_name, category_id, brand, price, cost_price, stock_quantity, weight_kg) VALUES
('گوشی سامسونگ گلکسی A52', 4, 'Samsung', 8500000, 7200000, 15, 0.189),
('گوشی شیائومی ردمی نوت 11', 4, 'Xiaomi', 6500000, 5500000, 25, 0.195),
('لپ تاپ لنوو ایده پد 3', 5, 'Lenovo', 25000000, 21000000, 8, 1.7),
('لپ تاپ ایسوس ویووبوک', 5, 'Asus', 32000000, 28000000, 5, 1.4),
('هدفون بلوتوث سونی WH-1000XM4', 6, 'Sony', 12000000, 9500000, 12, 0.254),
('ماوس وایرلس لاجیتک', 6, 'Logitech', 450000, 350000, 30, 0.089),
('پاوربانک شیائومی 20000 میلی آمپر', 6, 'Xiaomi', 800000, 600000, 40, 0.350),
('قهوه ساز فلر', 2, 'Philips', 3500000, 2800000, 18, 2.1),
('جاروبرقی سامسونگ', 2, 'Samsung', 4200000, 3500000, 10, 4.2)
ON CONFLICT DO NOTHING;

-- Insert orders
INSERT INTO orders (order_id, customer_id, order_date, total_amount, shipping_province, shipping_city, shipping_address, status, payment_method, payment_status) VALUES
(1, 1, '2023-12-01', 1500000, 'تهران', 'تهران', 'خیابان ولیعصر، پلاک ۱۲۳', 'delivered', 'online', 'paid'),
(2, 2, '2024-05-10', 8000000, 'اصفهان', 'اصفهان', 'چهارباغ عباسی، کوچه ۴۵', 'delivered', 'cash_on_delivery', 'paid'),
(3, 4, '2025-02-14', 4500000, 'آذربایجان شرقی', 'تبریز', 'خیابان امام، پلاک ۳۴', 'delivered', 'online', 'paid'),
(4, 5, '2025-08-05', 2000000, 'فارس', 'شیراز', 'خیابان زند، پلاک ۵۶', 'delivered', 'bank_transfer', 'paid'),
(5, 1, '2024-07-15', 8500000, 'تهران', 'تهران', 'خیابان انقلاب، پلاک ۸۹', 'delivered', 'online', 'paid'),
(6, 2, '2025-08-20', 12000000, 'اصفهان', 'اصفهان', 'چهارباغ عباسی، کوچه ۴۵', 'shipped', 'cash_on_delivery', 'pending'),
(7, 3, '2025-09-10', 25000000, 'خراسان رضوی', 'مشهد', 'بلوار وکیل آباد، پلاک ۶۷', 'delivered', 'bank_transfer', 'paid'),
(8, 1, '2025-10-26', 450000, 'تهران', 'تهران', 'خیابان ولیعصر، پلاک ۱۲۳', 'confirmed', 'online', 'paid'),
(9, 4, '2024-06-01', 6500000, 'آذربایجان شرقی', 'تبریز', 'خیابان امام، پلاک ۳۴', 'pending', 'cash_on_delivery', 'pending'),
(10, 5, '2025-10-20', 3500000, 'فارس', 'شیراز', 'خیابان زند، پلاک ۵۶', 'delivered', 'online', 'paid')
ON CONFLICT (order_id) DO NOTHING;

-- Insert order items
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(1, 7, 1, 1500000),
(2, 4, 1, 8000000),
(3, 6, 2, 2250000),
(4, 8, 1, 2000000),
(5, 1, 1, 8500000),
(6, 5, 1, 12000000),
(7, 3, 1, 25000000),
(8, 6, 1, 450000),
(9, 2, 1, 6500000),
(10, 8, 1, 3500000)
ON CONFLICT DO NOTHING;