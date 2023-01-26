from flask import Flask
from flask_cors import CORS, cross_origin
from website.views import views_blueprint
from website.request_handler import request_blueprint


def create_app():
    app = Flask(__name__, static_folder='../../client/build')

    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    app.register_blueprint(views_blueprint)
    app.register_blueprint(request_blueprint)

    return app
