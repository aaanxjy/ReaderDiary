from flask import Flask, render_template, request, redirect, url_for, flash
from extensions import db
from admin import admin
from forms import LoginForm, RegistrationForm
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user

from models import Book, db, User

from config import Config



app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
admin.init_app(app)
app.config['SECRET_KEY'] = 'idk'

with app.app_context():
    db.create_all()
    db.drop_all()
    db.create_all()
    hashed_password = generate_password_hash("12345678")
    admin = User(username = "Admin", password = hashed_password, rank = "Admin")
    db.session.add(admin)
    db.session.commit()

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


@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':

       if form.validate_on_submit():
           existing_user = User.query.filter_by(
               username=form.username.data
           ).first()
           if existing_user:
               flash("Користувач з таким ім'ям вже існує!", "danger")
               return redirect(url_for("register"))
        
           hashed_password = generate_password_hash(form.password.data)
           user = User(username=form.username.data, password=hashed_password, rank = "Client")

           db.session.add(user)
           db.session.commit()

           flash("Реєстрація пройшла успішно!", "success")
           login_user(user)
           return redirect(url_for("admin.index"))
    else:
       return render_template("register.html", form=form)

