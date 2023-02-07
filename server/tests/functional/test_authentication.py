import pytest
from flask_login import FlaskLoginClient
from website import create_app
from website.utilities.database import query_users_db


@pytest.fixture(scope='module')
def test_client():
    """ Initialise fixtures to allow reuse of objects across tests
    """
    flask_app = create_app()
    flask_app.test_client_class = FlaskLoginClient
    with flask_app.test_client(user=query_users_db(username='devuser5')) \
            as testing_client:
        with flask_app.app_context():
            yield testing_client
    return


def test_login_required_pages_when_logged_in(test_client):
    """ Tests if pages requiring login are accessible for a logged in user.
    """
    response = test_client.get('/welcome')
    assert response.status_code == 200
    return
