import pytest
import json
from website import create_app

# headers should indicate JSON for all post requests
mimetype = 'application/json'
headers = {'Content-Type': mimetype, 'Accept': mimetype}


@pytest.fixture(scope='module')
def test_client():
    """ Initialise fixtures to allow reuse of objects across tests
    """
    flask_app = create_app()
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client
    return


def test_home_page(test_client):
    """ Tests if homepage is working.
    """
    response = test_client.get('/')
    assert response.status_code == 200
    return

