CREATE DATABASE student_system;

USE student_system;

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    name VARCHAR(100),
    contact VARCHAR(50),
    email VARCHAR(100),
    city VARCHAR(50),
    department VARCHAR(50),
    student_id VARCHAR(50)
);
