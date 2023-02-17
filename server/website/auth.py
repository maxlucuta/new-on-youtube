from flask import Blueprint, request
from flask_login import login_user, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from .utilities.database import query_users_db, insert_user_into_db
from .utilities.users import User

auth_blueprint = Blueprint('auth_blueprint', __name__)


@auth_blueprint.route('/register', methods=['POST'])
def user_register():
    if current_user.is_authenticated:
        return {"message": "already logged in"}

    username = request.json["username"]
    password = request.json["password"]
    confirm_password = request.json["confirmation"]

    if not username or not password or password != confirm_password:
        return {"message": "invalid fields"}

    user = query_users_db(username=username)
    if user:
        return {"message": "username already in use"}

    hashed_pwd = generate_password_hash(password, method="pbkdf2:sha256",
                                        salt_length=8)
    new_user = User(-1, username, hashed_pwd,
                    ['placeholder_topic'], [])
    if insert_user_into_db(new_user):
        added_user = query_users_db(username=username)
        login_user(added_user, remember=True)
        return {"message": "successfully added and logged in"}

    return {"message": "unrecognised error"}


@auth_blueprint.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return {"message": "user already logged in"}

    username = request.json["username"]
    password = request.json["password"]

    if not username or not password:
        return {"message": "did not provide all fields"}

    user = query_users_db(username=username)
    if not user:
        return {"message": "username does not exist in db"}

    password_hash = user.password
    if not check_password_hash(password_hash, password):
        return {"message": "incorrect password"}

    login_user(user, remember=True)
    print(f"is_auth: {current_user.is_authenticated}")
    if current_user.is_authenticated:
        print(f"username: {current_user.username}")
    return {"message": "logged in"}


@auth_blueprint.route('/logged_in', methods=['POST'])
def logged_in():
    user = current_user.username if current_user.is_authenticated else ""
    return {"user": user}


@auth_blueprint.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return {"message": "logged out"}
