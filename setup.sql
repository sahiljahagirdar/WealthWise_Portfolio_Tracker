CREATE DATABASE portfolio;

CREATE TABLE users(
id SERIAL PRIMARY KEY,
name VARCHAR(100),
email VARCHAR(100) UNIQUE,
created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE transactions(
id SERIAL PRIMARY KEY,
user_id INT REFERENCES users(id) ON DELETE CASCADE,
symbol VARCHAR (20),
type VARCHAR(10) CHECK (type IN ('BUY','SELL')),
units NUMERIC (12,2),
price NUMERIC (12,2),
date DATE,
created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE prices(
symbol VARCHAR (20) PRIMARY KEY,
price NUMERIC (12,2),
updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE holdings(
id SERIAL PRIMARY KEY,
user_id INT REFERENCES users(id) ON DELETE CASCADE,
symbol VARCHAR (20),
units NUMERIC (12,2),
avg_cost NUMERIC (12,2),
updated_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO users(name, email)
VALUES ('Admin', 'admin@admin.com');