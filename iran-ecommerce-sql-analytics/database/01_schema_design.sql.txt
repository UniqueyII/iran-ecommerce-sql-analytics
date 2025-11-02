CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    national_code VARCHAR(10) UNIQUE,  -- کد ملی
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    province VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    phone VARCHAR(11) UNIQUE,          -- شماره همراه
    email VARCHAR(100),
    registration_date DATE DEFAULT CURRENT_DATE,
    birth_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    parent_category_id INTEGER REFERENCES categories(category_id),
    description TEXT
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(200) NOT NULL,
    category_id INTEGER REFERENCES categories(category_id),
    brand VARCHAR(100),
    price DECIMAL(12, 2) NOT NULL CHECK (price > 0),
    cost_price DECIMAL(12, 2) NOT NULL,
    stock_quantity INTEGER DEFAULT 0 CHECK (stock_quantity >= 0),
    weight_kg DECIMAL(5, 2),
    is_active BOOLEAN DEFAULT TRUE,
    created_date DATE DEFAULT CURRENT_DATE,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(12, 2) NOT NULL CHECK (total_amount > 0),
    shipping_province VARCHAR(50) NOT NULL,
    shipping_city VARCHAR(50) NOT NULL,
    shipping_address TEXT NOT NULL,
    status VARCHAR(20) CHECK (status IN ('pending', 'confirmed', 'shipped', 'delivered', 'cancelled')),
    payment_method VARCHAR(30) CHECK (payment_method IN ('online', 'cash_on_delivery', 'bank_transfer')),
    payment_status VARCHAR(20) CHECK (payment_status IN ('pending', 'paid', 'failed', 'refunded')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id),
    product_id INTEGER REFERENCES products(product_id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(12, 2) NOT NULL CHECK (unit_price > 0),
    line_total DECIMAL(12, 2) GENERATED ALWAYS AS (quantity * unit_price) STORED
);