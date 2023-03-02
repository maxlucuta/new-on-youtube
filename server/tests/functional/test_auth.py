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


def test_user_registration_with_no_username_returns_error(test_client):
    test_query = json.dumps({'username': "",
                             'password': "validpassword",
                             'confirmation': "validpassword",
                             'topics': "example_topics"})
    response = test_client.post("/register", data=test_query, headers=headers)
    response = json.loads(response.data)

    assert response['status_code'] == 400
    assert response['message'] == 'invalid fields'
    return


def test_user_registration_with_no_password_returns_error(test_client):
    test_query = json.dumps({'username': "validusername_fdhjalfdhjaslfjdsalfd",
                             'password': "",
                             'confirmation': "",
                             'topics': "example_topics"})
    response = test_client.post("/register", data=test_query, headers=headers)
    response = json.loads(response.data)

    assert response['status_code'] == 400
    assert response['message'] == 'invalid fields'
    return


def test_user_reg_with_none_matching_passwords_returns_error(test_client):
    test_query = json.dumps({'username': "validusername_fdhjalfdhjaslfjdsalfd",
                             'password': "invalidpassword",
                             'confirmation': "invalidpassword_different",
                             'topics': "example_topics"})
    response = test_client.post("/register", data=test_query, headers=headers)
    response = json.loads(response.data)

    assert response['status_code'] == 400
    assert response['message'] == 'invalid fields'
    return


def test_user_registration_with_taken_username_returns_error(test_client):
    test_query = json.dumps({'username': "devuser4",
                             'password': "validpassword",
                             'confirmation': "validpassword",
                             'topics': "example_topics"})
    response = test_client.post("/register", data=test_query, headers=headers)
    response = json.loads(response.data)

    assert response['status_code'] == 400
    assert response['message'] == 'username already in use'
    return


def test_user_registration_with_no_topics_returns_error(test_client):
    test_query = json.dumps({'username': "validusername_fdhjalfdhjaslfjdsalfd",
                             'password': "validpassword",
                             'confirmation': "validpassword",
                             'topics': ""})
    response = test_client.post("/register", data=test_query, headers=headers)
    response = json.loads(response.data)

    assert response['status_code'] == 400
    assert response['message'] == 'no topics selected'
    return


def test_user_login_with_no_username_returns_error(test_client):
    test_query = json.dumps({'username': "",
                             'password': "validpassword"})
    response = test_client.post("/login", data=test_query, headers=headers)
    response = json.loads(response.data)

    assert response['status_code'] == 400
    assert response['message'] == 'invalid fields'
    return


def test_user_login_with_no_password_returns_error(test_client):
    test_query = json.dumps({'username': "devuser4",
                             'password': ""})
    response = test_client.post("/login", data=test_query, headers=headers)
    response = json.loads(response.data)

    assert response['status_code'] == 400
    assert response['message'] == 'invalid fields'
    return


def test_user_login_with_invalid_username_returns_error(test_client):
    test_query = json.dumps({'username': "invalidusername_fdhjalfdhjaslfjlfd",
                             'password': "validpassword"})
    response = test_client.post("/login", data=test_query, headers=headers)
    response = json.loads(response.data)

    assert response['status_code'] == 400
    assert response['message'] == 'username not found'
    return


def test_user_login_with_incorrect_pwd_returns_error(test_client):
    test_query = json.dumps({'username': "devuser4",
                             'password': "incorrectpassword"})
    response = test_client.post("/login", data=test_query, headers=headers)
    response = json.loads(response.data)

    assert response['status_code'] == 400
    assert response['message'] == 'incorrect password'
    return


def test_user_login_with_valid_credentials_logs_user_in(test_client):
    test_query = json.dumps({'username': "devuser4",
                             'password': "password"})
    response = test_client.post("/login", data=test_query, headers=headers)
    response = json.loads(response.data)

    assert response['status_code'] == 200
    assert response['message'] == 'logged in'
    assert response['token']
    return
