CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    INDEX (email)
);

CREATE TABLE IF NOT EXISTS dashboards (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description VARCHAR(500),
    canvas_id VARCHAR(36) NOT NULL UNIQUE,
    owner_id INT,
    INDEX (id),
    FOREIGN KEY (owner_id) 
        REFERENCES users(id) 
        ON DELETE CASCADE
);