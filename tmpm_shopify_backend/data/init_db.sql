CREATE DATABASE IF NOT EXISTS shopify_backend;
USE shopify_backend;

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    inventory_count INT NOT NULL
);

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    status VARCHAR(255) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    discount DECIMAL(10, 2) NOT NULL,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products (id)
);
