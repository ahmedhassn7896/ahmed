CREATE TABLE IF NOT EXISTS transactions (
    transaction_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50),
    product_id VARCHAR(50),
    amount DECIMAL(10, 2),
    status VARCHAR(20),
    transaction_time TIMESTAMP
);

CREATE INDEX idx_transaction_time ON transactions(transaction_time);
