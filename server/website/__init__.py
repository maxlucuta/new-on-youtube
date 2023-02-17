import os
from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from website.views import views_blueprint
from website.request_handler import request_blueprint
from website.auth import auth_blueprint
from website.utilities.database import query_users_db, establish_connection
from website.utilities.subscriber import run_background_task
from threading import Thread


def create_app():
    if os.environ.get('IN_DOCKER_CONTAINER', False):
        app = Flask(__name__, static_folder='../static', static_url_path='/')
    else:
        app = Flask(__name__, static_folder='../../client/build')

    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.secret_key = "3ce02ed1f5e5d521adaf7ffca7a05703"

    login_manager = LoginManager()
    login_manager.login_view = 'auth_blueprint.login'
    login_manager.init_app(app)
    # login_manager.session_protection = "strong"
    # login_serializer = URLSafeTimedSerializer(app.secret_key)

    @login_manager.user_loader
    def load_user(user_id):
        print(f'load_user called with user_id: {user_id}')
        user = query_users_db(user_id=user_id)
        return user if user else None

    app.register_blueprint(views_blueprint)
    app.register_blueprint(request_blueprint)
    app.register_blueprint(auth_blueprint)

    global session
    session = establish_connection()

    Thread(name="background", target=run_background_task, daemon=True).start()

    return app
