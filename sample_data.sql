
INSERT INTO categories (category_name, parent_category_id, description) VALUES
('الکترونیک', NULL, 'کالاهای الکترونیکی'),
('خانه و آشپزخانه', NULL, 'لوازم خانه و آشپزخانه'),
('مد و پوشاک', NULL, 'لباس و پوشاک');


INSERT INTO categories (category_name, parent_category_id, description) VALUES
('موبایل و تبلت', 1, 'گوشی موبایل و تبلت'),
('لپ تاپ و کامپیوتر', 1, 'لپ تاپ و تجهیزات کامپیوتر'),
('لوازم جانبی', 1, 'لوازم جانبی الکترونیکی');


INSERT INTO customers (national_code, first_name, last_name, province, city, phone, email, birth_date) VALUES
('0123456769', 'علی', 'محمدی', 'تهران', 'تهران', '09121234667', 'ali.mohamadi@email.com', '1990-05-15'),
('1234567890', 'فاطمه', 'احمدی', 'اصفهان', 'اصفهان', '09123456789', 'fateme.ahmadi@email.com', '1992-08-22'),
('2345678901', 'محمد', 'کریمی', 'خراسان رضوی', 'مشهد', '09134567890', 'mohammad.karimi@email.com', '1988-12-10'),
('3456789012', 'زهرا', 'حسینی', 'آذربایجان شرقی', 'تبریز', '09145678901', 'zahra.hosseini@email.com', '1995-03-30'),
('4567890123', 'رضا', 'جعفری', 'فارس', 'شیراز', '09156789012', 'reza.jafari@email.com', '1993-07-18');


INSERT INTO products (product_name, category_id, brand, price, cost_price, stock_quantity, weight_kg) VALUES
('گوشی سامسونگ گلکسی A52', 2, 'Samsung', 8500000, 7200000, 15, 0.189),  -- category_id = 2 exists!
('گوشی شیائومی ردمی نوت 11', 2, 'Xiaomi', 6500000, 5500000, 25, 0.195),
('لپ تاپ لنوو ایده پد 3', 3, 'Lenovo', 25000000, 21000000, 8, 1.7),
('لپ تاپ ایسوس ویووبوک', 3, 'Asus', 32000000, 28000000, 5, 1.4),
('هدفون بلوتوث سونی WH-1000XM4', 4, 'Sony', 12000000, 9500000, 12, 0.254),
('ماوس وایرلس لاجیتک', 4, 'Logitech', 450000, 350000, 30, 0.089),
('پاوربانک شیائومی 20000 میلی آمپر', 4, 'Xiaomi', 800000, 600000, 40, 0.350),
('قهوه ساز فلر', 5, 'Philips', 3500000, 2800000, 18, 2.1),
('جاروبرقی سامسونگ', 5, 'Samsung', 4200000, 3500000, 10, 4.2);


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
(10, 5, '2025-10-20', 3500000, 'فارس', 'شیراز', 'خیابان زند، پلاک ۵۶', 'delivered', 'online', 'paid');


INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(1, 7, 1, 1500000),   -- Power bank
(2, 4, 1, 8000000),   -- Asus laptop  
(3, 6, 2, 2250000),   -- 2 mice
(4, 8, 1, 2000000),   -- Coffee maker
(5, 1, 1, 8500000),   -- Samsung phone
(6, 5, 1, 12000000),  -- Sony headphones
(7, 3, 1, 25000000),  -- Lenovo laptop
(8, 6, 1, 450000),    -- Mouse
(9, 2, 1, 6500000),   -- Xiaomi phone
(10, 8, 1, 3500000);  -- Coffee maker
