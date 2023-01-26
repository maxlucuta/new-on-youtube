from flask import Flask
from flask_cors import CORS, cross_origin
from flask_login import LoginManager
from website.views import views_blueprint
from website.request_handler import request_blueprint
from website.auth import auth_blueprint
from website.utilities.database import query_users_db
from website.utilities.users import User

def create_app():
    app = Flask(__name__)
    app.secret_key = "3ce02ed1f5e5d521adaf7ffca7a05703"

    login_manager = LoginManager()
    login_manager.login_view = 'auth_blueprint.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        user = query_users_db(user_id=user_id)
        return user if user else None

    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    app.register_blueprint(views_blueprint)
    app.register_blueprint(request_blueprint)
    app.register_blueprint(auth_blueprint)

    return app
