CREATE DATABASE business_db;
USE business_db;

CREATE TABLE listing_master (
  id INT AUTO_INCREMENT PRIMARY KEY,
  business_name VARCHAR(255) NOT NULL,
  category VARCHAR(100),
  city VARCHAR(100),
  address TEXT,
  phone VARCHAR(255),
  source VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_city ON listing_master(city);
CREATE INDEX idx_category ON listing_master(category);
CREATE INDEX idx_source ON listing_master(source);