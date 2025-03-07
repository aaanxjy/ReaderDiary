from flask import Flask, render_template, request, redirect, url_for

from models import Book, db

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
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
def edit_task():
#@app.route("/rate/<string:book_title>")
#def rate_book():
