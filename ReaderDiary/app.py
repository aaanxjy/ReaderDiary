from flask import Flask, render_template, request, redirect, url_for

from models import Book, db

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()
    db.drop_all()
    db.create_all()

@app.route("/")
def index():
    books = Book.query.all()
    return render_template("index.html", books = books)


@app.route("/add", methods = ['POST', 'GET'])
def add_book():
    if request.method == 'POST':
       title = request.form["title"].strip()
       author = request.form["author"].strip()
       description = request.form["description"].strip()
       #picture = request.form["pic"].strip()
       stars = int(request.form["stars"])
       new_book = Book(title = title, author = author, description = description, stars = stars) #picture = picture)
       db.session.add(new_book)
       db.session.commit()
       return redirect(url_for("index"))
    else:
       return render_template("newbook.html")

@app.route("/edit/<string:book_title>", methods = ['POST', 'GET'])
def edit_book(book_title):
    book = Book.query.get(book_title)
    if request.method == 'POST':
       book.title = request.form["title"].strip()
       book.author = request.form["author"].strip()
       book.description = request.form["description"].strip()
       #book.picture = request.form["pic"].strip()
       book.stars = int(request.form["stars"])
       db.session.commit()
       return redirect(url_for("index"))

    else:
        return render_template("editbook.html", book = book)
    

@app.route("/delete/<string:book_title>", methods = ['POST', 'GET'])
def delete_book(book_title):
    book = Book.query.get(book_title)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("index"))

#@app.route("/rate/<string:book_title>")
#def rate_book():
