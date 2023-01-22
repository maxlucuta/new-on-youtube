from flask import Blueprint
from .utilities.database import database_request

""" These can be split when they either get too big or we want to make 
    it easier to work in separate files"""

views_blueprint = Blueprint('views_blueprint', __name__)

@views_blueprint.route('/')
def landing_page():
    return "landing_page"

@views_blueprint.route('/database_test')
def database_test():
    return database_request()