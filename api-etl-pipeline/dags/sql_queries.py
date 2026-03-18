CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS dim_users (
    user_id SERIAL PRIMARY KEY,
    external_id VARCHAR(50) UNIQUE,
    full_name VARCHAR(100),
    email VARCHAR(100),
    country VARCHAR(50),
    last_updated TIMESTAMP
);
"""

UPSERT_USERS_SQL = """
INSERT INTO dim_users (external_id, full_name, email, country, last_updated)
VALUES %s
ON CONFLICT (external_id) DO UPDATE SET
    full_name = EXCLUDED.full_name,
    email = EXCLUDED.email,
    country = EXCLUDED.country,
    last_updated = EXCLUDED.last_updated;
"""
