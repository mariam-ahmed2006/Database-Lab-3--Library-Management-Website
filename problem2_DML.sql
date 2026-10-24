USE library;

-- Insert authors with their photo paths
INSERT INTO AUTHOR (name, country, image_url)
VALUES
    ('Naguib Mahfouz', 'Egypt', 'images/Naguib Mahfouz.jpg'),
    ('J.K. Rowling', 'United Kingdom', 'images/J.K. Rowling.jpg'),
    ('George Orwell', 'United Kingdom', 'images/George Orwell.jpg');

-- Insert books with their cover paths
INSERT INTO BOOK (title, price, author_id, image_url)
VALUES
    ('Palace Walk', 250.00, 1, 'images/Palace Walk.jpg'),
    ('The Thief and the Dogs', 180.00, 1, 'images/The Thief and the Dogs.jpg'),
    ('Harry Potter and the Philosophers Stone', 350.00, 2, 'images/Harry Potter and the Philosopher Stone.jpg'),
    ('Harry Potter and the Chamber of Secrets', 320.00, 2, 'images/Harry Potter and the Chamber of Secrets.jpg'),
    ('Animal Farm', 150.00, 3, 'images/Animal Farm.jpg'),
    ('Nineteen Eighty-Four', 200.00, 3, 'images/Nineteen Eighty-Four.jpg');

