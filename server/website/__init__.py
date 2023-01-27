from flask import Flask
from flask_cors import CORS, cross_origin
from .views import views_blueprint
from .request_handler import request_blueprint
from .utilities.subscriber import process_tasks
from threading import Thread

def create_app():
    
    app = Flask(__name__)
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    app.register_blueprint(views_blueprint)
    app.register_blueprint(request_blueprint)

    Thread(name="background", target=process_tasks, daemon=True).start()

    return app
