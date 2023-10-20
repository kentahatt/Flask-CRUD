from . import db
from flask_login import UserMixin

# The Student class represents a table in a SQL database. It uses the SQLAlchemy
# library to interact with the database. This class has fields for id, name, email, and phone,
# and provides an initializer method to set the values of these fields.


class Student(db.Model):

    # __tablename__ defines the name of the table in SQL (Check phpmyadmin for clarity)
    __tablename__ = 'students'

    # Setting id as the primary key
    # Nullable=False means that specific data can't be NULL
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80), nullable=False)

    def __init__(self, name, email, phone):

        self.name = name
        self.email = email
        self.phone = phone


# UserMixin allows us to use methods such as is_authenticated(), is_active(),
# is_anonymous(), and get_id()
class LoginUser(UserMixin, db.Model):

    __tablename__ = 'Login-Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pw = db.Column(db.String(300), unique=True, nullable=False)

    def __init__(self, username, email, pw):
        self.username = username
        self.email = email
        self.pw = pw
