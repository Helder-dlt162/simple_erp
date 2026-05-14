CREATE TABLE 
    IF NOT EXISTS user_types (
        id SERIAL PRIMARY KEY,
        name VARCHAR(32) UNIQUE NOT NULL,
        type_id VARCHAR(4) UNIQUE NOT NULL,
        modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

-- seed data for user_types
INSERT INTO user_types (name, type_id)
    VALUES ('Administrator', '0001');

CREATE TABLE
    IF NOT EXISTS employees (
        id SERIAL PRIMARY KEY,
        employee_id VARCHAR(16) UNIQUE NOT NULL,
        first_name VARCHAR(32) NOT NULL,
        last_name VARCHAR(32),
        cpf VARCHAR(14) UNIQUE,
        birth_date DATE,
        department VARCHAR(32),
        modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

CREATE TABLE
    IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(32) UNIQUE NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        user_type VARCHAR(8) NOT NULL,
        employee_id VARCHAR(32) UNIQUE,
        modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
        FOREIGN KEY (user_type) REFERENCES user_types(type_id)

    );

