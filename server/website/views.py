import os
from flask import Blueprint, send_from_directory
from .utilities.database import database_request

""" These can be split when they either get too big or we want to make 
    it easier to work in separate files"""

views_blueprint = Blueprint('views_blueprint', __name__, static_folder='../../client/build')

@views_blueprint.route('/', defaults={'path': ''})
@views_blueprint.route('/<path:path>')
def landing_page(path):
    if path != "" and os.path.exists(views_blueprint.static_folder + '/' + path):
        return send_from_directory(views_blueprint.static_folder, path)
    else:
        return send_from_directory(views_blueprint.static_folder, 'index.html')

@views_blueprint.route('/database_test')
def database_test():
    return database_request()