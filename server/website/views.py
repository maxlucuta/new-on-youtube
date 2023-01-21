from flask import Blueprint

import website.models as db


""" These can be split when they either get too big or we want to make 
    it easier to work in separate files"""

landing_page = Blueprint('landing_page', __name__)
database_test = Blueprint('database_test', __name__)


@landing_page.route('/')
def blueprint():
    return "landing_page"


@database_test.route('/database_test')
def blueprint():
    return db.database_request()