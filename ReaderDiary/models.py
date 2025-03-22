from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from extensions import db

class Book(db.Model):
    __tablename__ = "books" 
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String,)
    picture = db.Column(db.String)
    author = db.Column(db.String, nullable = False)
    description = db.Column(db.String, nullable = False)
    stars = db.Column(db.Integer)
    user = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)



class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    rank = db.Column(db.String, nullable = False)






