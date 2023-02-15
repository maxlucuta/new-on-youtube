from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from .utilities.database import query_users_db, insert_user_into_db
from .utilities.users import User

auth_blueprint = Blueprint('auth_blueprint', __name__)


@auth_blueprint.route('/register', methods=['POST'])
def user_register():
    if current_user.is_authenticated:
        flash('You are already logged in. Go to /logout to logout')
        return {"message": "already logged in"}

    username = request.json["username"]
    password = request.json["password"]
    confirm_password = request.json["confirmation"]

    if not username or not password or password != confirm_password:
        flash("""Please enter a username, password and matching password
                confirmation""")
        return {"message": "invalid fields"}

    user = query_users_db(username=username)
    if user:
        flash('Username already exists, please enter a different username')
        return {"message": "already exists"}

    hashed_pwd = generate_password_hash(password, method="pbkdf2:sha256",
                                        salt_length=8)
    new_user = User(-1, username, hashed_pwd,
                    ['placeholder_category'], ['placeholder_channel'])
    if insert_user_into_db(new_user):
        flash('Successfully registered, please login!')
        return {"message": "successfully added"}

    flash('Registration unsuccessful, please try again')
    return {"message": "unrecognised error"}


@auth_blueprint.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in. Go to /logout to logout')
        return {"message": "already logged in"}

    username = request.json["username"]
    password = request.json["password"]

    if not username or not password:
        flash('Please enter a username and password')
        return {"message": "invalid fields"}

    user = query_users_db(username=username)
    if not user:
        flash('Username does not exist')
        return {"message": "no username"}

    password_hash = user.password
    if not check_password_hash(password_hash, password):
        flash('Password is incorrect')
        return {"message": "incorrect password"}

    login_user(user, remember=True)
    flash('Logged in successfully')
    return {"message": "logged in"}


@auth_blueprint.route('/welcome')
@login_required
def welcome():
    return render_template('profile.html', username=current_user.username)


@auth_blueprint.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return {"message": "logged out"}
