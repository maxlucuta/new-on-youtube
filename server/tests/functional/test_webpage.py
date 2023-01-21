import pytest
from website import create_app

# use of fixture to allow us to reuse objects across tests
@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client

def test_home_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 200

def test_database_test_page(test_client):
    response = test_client.get('/database_test')
    assert response.status_code == 200