-- Vignan TechSolutions - Database Setup Script
-- Run this in MySQL Workbench or MySQL CLI

CREATE DATABASE IF NOT EXISTS vignan_techsolutions
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE vignan_techsolutions;

-- Grant permissions (change 'your_password' to your actual password)
-- CREATE USER IF NOT EXISTS 'vignan_user'@'localhost' IDENTIFIED BY 'your_password';
-- GRANT ALL PRIVILEGES ON vignan_techsolutions.* TO 'vignan_user'@'localhost';
-- FLUSH PRIVILEGES;

SELECT 'Database vignan_techsolutions created successfully!' AS Status;
