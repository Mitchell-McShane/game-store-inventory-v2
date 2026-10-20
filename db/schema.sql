-- Game Store Inventory Manager 2.0
-- Database Schema

CREATE TABLE publishers (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE games (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    platform VARCHAR(100) NOT NULL,
    stock_quantity INTEGER NOT NULL DEFAULT 0,
    buying_cost NUMERIC(10, 2) NOT NULL,
    selling_price NUMERIC(10, 2) NOT NULL,
    publisher_id BIGINT NOT NULL REFERENCES publishers(id),

    CONSTRAINT positive_stock CHECK (stock_quantity >= 0),
    CONSTRAINT positive_buying_cost CHECK (buying_cost >= 0),
    CONSTRAINT positive_selling_price CHECK (selling_price >= 0)
);