import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from website.views import views_blueprint
from website.request_handler import request_blueprint
from website.auth import auth_blueprint
from website.utilities.database import establish_connection
from website.utilities.pubsub.subscriber import run_background_task
from website.utilities.pubsub.publisher import Publisher
from threading import Thread
from flask_jwt_extended import JWTManager
from datetime import timedelta
from cassandra.query import dict_factory
from website.utilities.recommender import Recommender


def create_app():
    if os.environ.get('IN_DOCKER_CONTAINER', False):
        app = Flask(__name__, static_folder='../static', static_url_path='/')
        Thread(name="background1",
               target=run_background_task,
               daemon=True).start()
        Thread(name="background2",
               target=run_background_task,
               daemon=True).start()
    else:
        app = Flask(__name__, static_folder='../../client/build')

    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config["JWT_SECRET_KEY"] = \
        "this-ranch-aint-big-enough-for-the-two-of-us"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.secret_key = "3ce02ed1f5e5d521adaf7ffca7a05703"

    JWTManager(app)
    CORS(app)

    app.register_blueprint(views_blueprint)
    app.register_blueprint(request_blueprint)
    app.register_blueprint(auth_blueprint)

    def not_found_handler(e):
        return send_from_directory(app.static_folder, 'index.html'), 404
    app.register_error_handler(404, not_found_handler)

    global publisher
    publisher = Publisher()

    global session
    session = establish_connection()
    session.row_factory = dict_factory

    global recommender
    recommender = Recommender()
    recommender.train_model()

    return app
