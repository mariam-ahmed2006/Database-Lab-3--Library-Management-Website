
# Database Systems Lab 3

## Requirements

- MySQL Server
- MySQL Workbench
- Python 3
- Visual Studio Code

## 1. Create the databases

Open MySQL Workbench and execute these files in order:

1. `problem1_DDL.sql`
2. `problem1_DML.sql`
3. `problem2_DDL.sql`
4. `problem2_DML.sql`

The DDL files create the databases and tables. The DML files insert sample data.

## 2. Configure the website

Open a terminal in the `website` directory.

Create a `.env` file with your local database credentials:

- DB_HOST=localhost
- DB_USER=root
- DB_PASSWORD=your_mysql_password
- DB_NAME=library

Do not commit `.env` to GitHub.

## 3. Install dependencies

Create and activate a Python virtual environment, then run:

    python -m pip install -r requirements.txt

## 4. Run the website

Run:

    python app.py

Open http://127.0.0.1:5000 in your browser.

## 5. Website features

- Display all books and authors
- Add books and authors
- Edit books and authors
- Delete books
- Delete authors and their associated books
