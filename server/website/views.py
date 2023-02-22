import os
from flask import Blueprint, send_from_directory

views_blueprint = Blueprint('views_blueprint', __name__,
                            static_folder='./static',
                            static_url_path='/') if \
    os.environ.get('IN_DOCKER_CONTAINER', False) else \
    Blueprint('views_blueprint', __name__, static_folder='../../client/build')


@views_blueprint.route('/', defaults={'path': ''})
@views_blueprint.route('/<path:path>')
def landing_page(path):
    if path != "" and os.path.exists(views_blueprint.static_folder +
                                     '/' + path):
        return send_from_directory(views_blueprint.static_folder, path)
    else:
        return send_from_directory(views_blueprint.static_folder, 'index.html')
