from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
import os
import uuid
from decimal import Decimal, InvalidOperation
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "local-development-key")


def get_db():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "library"),
        cursorclass=pymysql.cursors.DictCursor
    )

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "gif"}

def save_uploaded_image(field_name):
    image = request.files.get(field_name)

    if not image or image.filename == "":
        return None

    original_name = secure_filename(image.filename)

    if "." not in original_name:
        raise ValueError("Please upload a valid image file.")

    extension = original_name.rsplit(".", 1)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            "Only JPG, JPEG, PNG, WEBP, and GIF images are allowed."
        )

    image_folder = os.path.join(
        app.root_path, "static", "images"
    )
    os.makedirs(image_folder, exist_ok=True)

    filename = f"{uuid.uuid4().hex}.{extension}"
    image_path = os.path.join(image_folder, filename)

    image.save(image_path)

    return f"images/{filename}"


@app.route("/")
def index():
    db = get_db()
    try:
        with db.cursor() as cursor:
            # Get all books together with their author names
            cursor.execute("""
                SELECT
                    BOOK.book_id,
                    BOOK.image_url,
                    BOOK.title,
                    BOOK.price,
                    BOOK.author_id,
                    AUTHOR.name AS author_name
                FROM BOOK
                INNER JOIN AUTHOR
                    ON BOOK.author_id = AUTHOR.author_id
                ORDER BY BOOK.book_id DESC
            """)
            books = cursor.fetchall()

            # Get all authors
            cursor.execute("""
                SELECT *
                FROM AUTHOR
                ORDER BY author_id
            """)
            authors = cursor.fetchall()

            # Calculate dashboard statistics
            cursor.execute("""
                SELECT
                    COUNT(*) AS total_books,
                    COALESCE(AVG(price), 0) AS average_price
                FROM BOOK
            """)
            book_stats = cursor.fetchone()

            cursor.execute("""
                SELECT
                    COUNT(*) AS total_authors,
                    COUNT(DISTINCT country) AS total_countries
                FROM AUTHOR
            """)
            author_stats = cursor.fetchone()

        return render_template(
            "index.html",
            books=books,
            authors=authors,
            total_books=book_stats["total_books"],
            average_price=book_stats["average_price"],
            total_authors=author_stats["total_authors"],
            total_countries=author_stats["total_countries"]
        )
    finally:
        db.close()


@app.route("/authors/add", methods=["GET", "POST"])
def add_author():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        country = request.form.get("country", "").strip()

        if not name or not country:
            flash("Name and country are required.")
            return redirect(url_for("add_author"))

        try:
            image_url = save_uploaded_image("image")
        except ValueError as error:
            flash(str(error))
            return redirect(url_for("add_author"))

        db = get_db()
        try:
            with db.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO AUTHOR (name, country, image_url)
                       VALUES (%s, %s, %s)""",
                    (name, country, image_url)
                )
            db.commit()
        finally:
            db.close()

        flash("Author added successfully.")
        return redirect(url_for("index"))

    return render_template("author_form.html", author=None)




@app.route("/authors/edit/<int:author_id>", methods=["GET", "POST"])
def edit_author(author_id):
    db = get_db()
    try:
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM AUTHOR WHERE author_id = %s",
                (author_id,)
            )
            author = cursor.fetchone()

            if author is None:
                return "Author not found", 404

            if request.method == "POST":
                name = request.form.get("name", "").strip()
                country = request.form.get("country", "").strip()

                if not name or not country:
                    flash("Name and country are required.")
                    return redirect(
                        url_for("edit_author", author_id=author_id)
                    )

                try:
                    new_image_url = save_uploaded_image("image")
                except ValueError as error:
                    flash(str(error))
                    return redirect(
                        url_for("edit_author", author_id=author_id)
                    )

                # Keep the current photo if no new one was uploaded
                image_url = new_image_url or author.get("image_url")

                cursor.execute(
                    """UPDATE AUTHOR
                       SET name = %s, country = %s, image_url = %s
                       WHERE author_id = %s""",
                    (name, country, image_url, author_id)
                )
                db.commit()

                flash("Author updated successfully.")
                return redirect(url_for("index"))

            return render_template("author_form.html", author=author)
    finally:
        db.close()


@app.route("/books/add", methods=["GET", "POST"])
def add_book():
    db = get_db()
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM AUTHOR ORDER BY name")
            authors = cursor.fetchall()

            if request.method == "POST":
                title = request.form.get("title", "").strip()
                price_text = request.form.get("price", "")
                author_id = request.form.get("author_id", "")

                try:
                    price = Decimal(price_text)
                    if not price.is_finite() or price < 0:
                        raise InvalidOperation
                except (InvalidOperation, ValueError):
                    flash("Enter a valid non-negative price.")
                    return redirect(url_for("add_book"))

                if not title or not author_id:
                    flash("Title and author are required.")
                    return redirect(url_for("add_book"))

                cursor.execute(
                    "SELECT author_id FROM AUTHOR WHERE author_id = %s",
                    (author_id,)
                )
                if cursor.fetchone() is None:
                    flash("Please select an existing author.")
                    return redirect(url_for("add_book"))

                try:
                    image_url = save_uploaded_image("image")
                except ValueError as error:
                    flash(str(error))
                    return redirect(url_for("add_book"))

                cursor.execute(
                    """INSERT INTO BOOK
                       (title, price, author_id, image_url)
                       VALUES (%s, %s, %s, %s)""",
                    (title, price, author_id, image_url)
                )
                db.commit()
                flash("Book added successfully.")
                return redirect(url_for("index"))

            return render_template(
                "book_form.html", book=None, authors=authors
            )
    finally:
        db.close()




@app.route("/books/edit/<int:book_id>", methods=["GET", "POST"])
def edit_book(book_id):
    db = get_db()
    try:
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM BOOK WHERE book_id = %s",
                (book_id,)
            )
            book = cursor.fetchone()

            if book is None:
                return "Book not found", 404

            cursor.execute("SELECT * FROM AUTHOR ORDER BY name")
            authors = cursor.fetchall()

            if request.method == "POST":
                title = request.form.get("title", "").strip()
                price_text = request.form.get("price", "")
                author_id = request.form.get("author_id", "")

                try:
                    price = Decimal(price_text)
                    if not price.is_finite() or price < 0:
                        raise InvalidOperation
                except (InvalidOperation, ValueError):
                    flash("Enter a valid non-negative price.")
                    return redirect(
                        url_for("edit_book", book_id=book_id)
                    )

                if not title or not author_id:
                    flash("Title and author are required.")
                    return redirect(
                        url_for("edit_book", book_id=book_id)
                    )

                cursor.execute(
                    "SELECT author_id FROM AUTHOR WHERE author_id = %s",
                    (author_id,)
                )
                if cursor.fetchone() is None:
                    flash("Please select an existing author.")
                    return redirect(
                        url_for("edit_book", book_id=book_id)
                    )

                try:
                    new_image_url = save_uploaded_image("image")
                except ValueError as error:
                    flash(str(error))
                    return redirect(
                        url_for("edit_book", book_id=book_id)
                    )

                # Keep the current cover if no new image was uploaded
                image_url = new_image_url or book.get("image_url")

                cursor.execute(
                    """UPDATE BOOK
                       SET title = %s,
                           price = %s,
                           author_id = %s,
                           image_url = %s
                       WHERE book_id = %s""",
                    (title, price, author_id, image_url, book_id)
                )
                db.commit()

                flash("Book updated successfully.")
                return redirect(url_for("index"))

            return render_template(
                "book_form.html", book=book, authors=authors
            )
    finally:
        db.close()



@app.route("/books/delete/<int:book_id>", methods=["POST"])
def delete_book(book_id):
    db = get_db()
    try:
        with db.cursor() as cursor:
            cursor.execute(
                "DELETE FROM BOOK WHERE book_id = %s", (book_id,)
            )
        db.commit()
    finally:
        db.close()

    flash("Book deleted.")
    return redirect(url_for("index"))


@app.route("/authors/delete/<int:author_id>", methods=["POST"])
def delete_author(author_id):
    db = get_db()
    try:
        with db.cursor() as cursor:
            cursor.execute(
                "DELETE FROM AUTHOR WHERE author_id = %s", (author_id,)
            )
        db.commit()
    finally:
        db.close()

    flash("Author and their books deleted.")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
