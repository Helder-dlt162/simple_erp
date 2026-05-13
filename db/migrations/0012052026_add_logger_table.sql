CREATE TYPE log_level AS ENUM (
    'DEBUG',
    'INFO',
    'WARNING',
    'ERROR',
    'CRITICAL'
);

CREATE TABLE IF NOT EXISTS logger (
    id SERIAL PRIMARY KEY,
    level log_level NOT NULL,
    message TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);