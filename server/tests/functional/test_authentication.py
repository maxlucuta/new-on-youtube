import pytest
from flask_login import FlaskLoginClient
from website import create_app
from website.utilities.database import query_users


@pytest.fixture(scope='module')
def test_client():
    """ Initialise fixtures to allow reuse of objects across tests
    """
    flask_app = create_app()
    flask_app.test_client_class = FlaskLoginClient
    with flask_app.test_client(user=query_users(username='devuser5')) \
            as testing_client:
        with flask_app.app_context():
            yield testing_client
    return
