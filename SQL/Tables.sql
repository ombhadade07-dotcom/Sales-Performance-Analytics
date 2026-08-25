-- ============================================================
-- Sales Performance Analytics — Database Schema
-- MySQL syntax. Run this once before loading the insert_*.sql files.
-- ============================================================

CREATE DATABASE IF NOT EXISTS sales_analytics_db;
USE sales_analytics_db;

-- Drop in dependency order so re-running this file is safe
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS shipping;

CREATE TABLE customers (
    customer_id   VARCHAR(20) PRIMARY KEY NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    segment       VARCHAR(50) NOT NULL
);

CREATE TABLE products (
    product_id   VARCHAR(30) PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category     VARCHAR(50) NOT NULL,
    sub_category VARCHAR(50) NOT NULL
);

CREATE TABLE locations (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    postal_code VARCHAR(20),
    city        VARCHAR(100) NOT NULL,
    country     VARCHAR(100) NOT NULL
);

CREATE TABLE shipping (
    shipping_id    INT AUTO_INCREMENT PRIMARY KEY,
    ship_mode      VARCHAR(50) NOT NULL,
    order_priority VARCHAR(30) NOT NULL
);

CREATE TABLE orders (
    row_id        INT PRIMARY KEY,
    order_id      VARCHAR(25) NOT NULL,
    order_date    DATE NOT NULL,
    ship_date     DATE NOT NULL,
    customer_id   VARCHAR(20) NOT NULL,
    product_id    VARCHAR(30) NOT NULL,
    location_id   INT NOT NULL,
    shipping_id   INT NOT NULL,
    sales         DECIMAL(10,2) NOT NULL,
    quantity      INT NOT NULL,
    discount      DECIMAL(5,2) NOT NULL,
    profit        DECIMAL(10,2) NOT NULL,
    shipping_cost DECIMAL(10,2) NOT NULL,

    CONSTRAINT fk_customer
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    CONSTRAINT fk_product
        FOREIGN KEY (product_id) REFERENCES products(product_id),
    CONSTRAINT fk_location
        FOREIGN KEY (location_id) REFERENCES locations(location_id),
    CONSTRAINT fk_shipping
        FOREIGN KEY (shipping_id) REFERENCES shipping(shipping_id)
);

-- Sanity check after loading the insert_*.sql files
SHOW TABLES;
