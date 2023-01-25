from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from website.models import query_db, insert_db, User

auth_blueprint = Blueprint('auth_blueprint', __name__)

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def user_register():
    if current_user.is_authenticated:
        flash('You are already logged in. Go to /logout to logout')
        return redirect('/welcome')

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmation")

        if not username or not password or password != confirm_password:
            flash('Please enter a username, password and matching password confirmation')
            return render_template("register.html")

        user = query_db('SELECT * FROM users WHERE username = ?', [username], one=True)
        if user:
            flash('Username already exists, please enter a different username')
            return render_template("register.html")

        hashed_pwd = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)
        insert_db('INSERT INTO users (username, password) VALUES (?, ?)', [username, hashed_pwd])
        return redirect('/login')
    
    else:
        return render_template("register.html")

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in. Go to /logout to logout')
        return redirect('/welcome')

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash('Please enter a username and password')
            return render_template("login.html")

        user = query_db('SELECT * FROM users WHERE username = ?', [username], one=True)
        if not user:
            flash('Username does not exist')
            return render_template("login.html")

        password_hash = user['password']
        if not check_password_hash(password_hash, password):
            flash('Password is incorrect')
            return render_template("login.html")

        user_obj = User(user['id'], user['username'], user['password'])
        login_user(user_obj, remember=True)
        flash('Logged in successfully')

        return redirect('/welcome')

    else:
        return render_template("login.html")

@auth_blueprint.route('/welcome')
@login_required
def welcome():
    return render_template('profile.html', username=current_user.username)

@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')