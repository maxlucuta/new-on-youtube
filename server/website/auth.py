from flask import Blueprint, request
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity
from datetime import timedelta, timezone, datetime
import json
from .utilities.database import query_users
from .utilities.database import insert_user
from .utilities.database import add_videos_to_queue
from .utilities.users import User

auth_blueprint = Blueprint('auth_blueprint', __name__)


@auth_blueprint.route('/register', methods=['POST'])
def user_register():

    username = request.json["username"]
    password = request.json["password"]
    confirm_password = request.json["confirmation"]
    topics = request.json["topics"]

    if not username or not password or password != confirm_password:
        return {"status_code": 400, "message": "invalid fields", "token": ""}

    print(username, "attempting to register")
    user = query_users(username=username)
    if user:
        return {
            "status_code": 400,
            "message": "username already in use",
            "token": ""
        }

    if not topics:
        return {"message": "no topics selected"}

    hashed_pwd = generate_password_hash(password, method="pbkdf2:sha256",
                                        salt_length=8)
    new_user = User(-1, username, hashed_pwd, topics)
    if insert_user(new_user):
        token = create_access_token(identity=username)
        add_videos_to_queue(topics)
        return {
            "status_code": 400,
            "message": "successfully added and logged in",
            "token": token
        }

    return {"status_code": 405, "message": "unrecognised error"}


@auth_blueprint.route('/login', methods=['POST'])
def login():

    username = request.json["username"]
    password = request.json["password"]

    if not username or not password:
        print("bad input!--------------")
        return {
            "status_code": 400,
            "message": "invalid fields",
            "token": ""
        }

    user = query_users(username=username)
    if not user:
        print("no user!--------------")
        return {
            "status_code": 400,
            "message": "username not found",
            "token": ""
        }

    password_hash = user.password
    if not check_password_hash(password_hash, password):
        print("incorrect pass--------------")
        return {
            "status_code": 400,
            "message": "incorrect password",
            "token": ""
        }

    token = create_access_token(identity=username)
    print(username, "logged in.")
    return {"status_code": 200, "message": "logged in", "token": token}


@auth_blueprint.after_app_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))

        if target_timestamp > exp_timestamp:
            token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["token"] = token
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        # routes that do not require jwt authentication
        return response
