from flask import Flask, render_template, request, redirect, url_for, flash, request, make_response 
from extensions import db, login_manager
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
login_manager.init_app(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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
def homepage():
    return redirect(url_for("register"))


@app.route("/account")
def index():
    user = int(request.cookies.get('UserId'))
    books = [book for book in Book.query.all() if book.user == user]
    if books:
       print(books[0].title)
    return render_template("index.html", books = books)


@app.route('/setcookie/<string:user_id>', methods = ['POST', 'GET'])
def setcookie(user_id):
   if load_user(user_id).rank == "Admin":
       resp = redirect(url_for("admin.index"))
   else:
       resp = redirect(url_for("index"))

   resp.set_cookie('UserId', user_id)

   return resp

@app.route("/add", methods = ['POST', 'GET'])
def add_book():
    if request.method == 'POST':
       title = request.form["title"].strip()
       author = request.form["author"].strip()
       description = request.form["description"].strip()
       #picture = request.form["pic"].strip()
       stars = int(request.form["stars"])
       user = request.cookies.get('UserId') 
       new_book = Book(title = title, author = author, description = description, stars = stars, user = user) #picture = picture)
       db.session.add(new_book)
       db.session.commit()
       return redirect(url_for("index"))
    else:
       return render_template("newbook.html")

@app.route("/edit/<string:book_id>", methods = ['POST', 'GET'])
def edit_book(book_id):
    book = Book.query.get(book_id)
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
    

@app.route("/delete/<string:book_id>", methods = ['POST', 'GET'])
def delete_book(book_id):
    book = Book.query.get(book_id)
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
           return redirect(url_for("setcookie", user_id = user.id))
    else:
       return render_template("register.html", form=form)
    

@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':

       if form.validate_on_submit():
           user = User.query.filter_by(
               username=form.username.data
           ).first()
           if user and check_password_hash(user.password, form.password.data):
               login_user(user)
               flash("Вхід пройшов успішно!", "success")
               return redirect(url_for("setcookie", user_id = user.id))
           else:
               flash("Неправильне ім'я користувача або пароль", "danger")
               return redirect(url_for("login"))
    else:
       return render_template("login.html", form=form)
    

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("homepage"))



