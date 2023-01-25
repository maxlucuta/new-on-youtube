from flask import Blueprint


views_blueprint = Blueprint('views_blueprint', __name__)

@views_blueprint.route('/')
def landing_page():
    return "landing_page"