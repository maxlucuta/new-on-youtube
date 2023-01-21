from flask import Flask
from flask_cors import CORS, cross_origin

from website.views import landing_page
from website.views import database_test


def create_app():
    app = Flask(__name__)

    # need to enable cross origin requests for development
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    app.register_blueprint(landing_page)
    app.register_blueprint(database_test)

    return app