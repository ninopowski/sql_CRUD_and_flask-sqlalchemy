import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# db = sqlite3.connect('library.db')
#
# cursor = db.cursor()
#
# cursor.execute("CREATE TABLE books "
#                "(id INTEGER PRIMARY KEY,"
#                "title VARCHAR(250) NOT NULL UNIQUE,"
#                "author VARCHAR(250) NOT NULL,"
#                "rating FLOAT NOT NULL) ")
#
# cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J.K. Rolling', 9.8)")
# db.commit()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new_books_collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    author = db.Column(db.String(150), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f" Title: {self.title}, by: {self.author}, with {self.rating} rating."

db.create_all()

# CRUD

# Create
# new_book = Book(title="Batman", author="Stan Lee", rating=8.7)
# db.session.add(new_book)
# db.session.commit()

# Read
# all_books = db.session.query(Book).all()
# print(all_books)

# read particular record
# book = Book.query.filter_by(title='Batman').first()
# print(book)

# Update by query
# book_to_update = Book.query.filter_by(title='Batman').first()
# book_to_update.title = 'Me'
# db.session.commit()

# update by id
# book_id = 2
# update_by_id = Book.query.get(book_id)
# update_by_id.title = 'Queen'
# db.session.commit()

# Deleting entries
# book_to_delete_id = 2
# book_to_delete = Book.query.get(book_to_delete_id)
# db.session.delete(book_to_delete)
# db.session.commit()


@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    return render_template("index.html", books=all_books)


@app.route('/add', methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = Book(
            title=request.form['title'],
            author=request.form['author'],
            rating=request.form['rating']
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")

@app.route('/edit-rating', methods=["GET", "POST"])
def edit_rating():
    if request.method == "POST":
        # update record
        book_id = request.form['id']
        book_to_update = Book.query.get(book_id)
        book_to_update.rating = request.form['rating']
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_selected = Book.query.get(book_id)
    return render_template("edit.html", book=book_selected)

@app.route('/delete', methods=["GET", "POST"])
def delete_entry():
    book_id = request.args.get('id')
    book_to_delete = Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()

    return redirect(url_for('home'))



if __name__ == "__main__":
    app.run(debug=True)

