from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import LoginUser
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/')
def reroute_login():
    return redirect(url_for('auth.login'))


@auth.route('/login')
def login():
    return render_template('auth/login.html')


# login_post() handles a POST request to the '/login' endpoint.
# It retrieves the email and password from the request form, checks if the user exists in the database,
# and verifies the password using password hashing. If the user does not exist or the password is incorrect,
# it displays an error message and redirects the user back to the login page. If the login is successful,
# it logs the user in and redirects them to the 'get_students' endpoint.
@auth.route('/login', methods=['POST'])
def login_post():
    # login code
    email = request.form.get('email')
    pw = request.form.get('pw')
    remember = True if request.form.get('remember') else False

    user = LoginUser.query.filter_by(email=email).first()

    # check if user exists
    # password hashing
    if not user:
        flash('User not found, Please try again')
        return redirect(url_for('auth.login'))

    if not check_password_hash(user.pw, pw):
        flash('Incorrect Password, Please try again')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.get_students'))


@auth.route('/signup')
def signup():
    return render_template('auth/signup.html')


# signup_post() handles the POST request for the '/signup' endpoint.
# It validates the user input, checks if the email address already exists in the database,
# and adds a new user to the database if the email address is unique.
@auth.route('/signup', methods=['POST'])
def signup_post():
    # validating and adding user to database
    username = request.form['username']
    email = request.form['email']
    pw = generate_password_hash(request.form['pw'], method='scrypt')

    user = LoginUser.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.login'))

    # Creating a new user with form data, hashing password for security
    # SHA-256 stands for Secure Hash Algorithm 256-bit, and it's used for cryptographic security
    new_user = LoginUser(username, email, pw)

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out')
    return redirect(url_for('auth.login'))
