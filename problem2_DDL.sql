DROP DATABASE IF EXISTS library;
CREATE DATABASE library;
USE library;

-- Create the AUTHOR table first
CREATE TABLE AUTHOR (
    author_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(50) NOT NULL,
    image_url VARCHAR(255) NULL
);

-- Create the BOOK table
CREATE TABLE BOOK (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    author_id INT NOT NULL,
    image_url VARCHAR(255) NULL,
    CONSTRAINT fk_book_author
        FOREIGN KEY (author_id)
        REFERENCES AUTHOR(author_id)
        ON DELETE CASCADE
);

