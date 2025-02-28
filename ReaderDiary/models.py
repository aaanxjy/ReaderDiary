from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    title = db.Column(db.String, primary_key = True)
    picture = db.Column(db.String)
    author = db.Column(db.String, nullable = False)
    description = db.Column(db.String)
    stars = db.Column(db.Integer)




