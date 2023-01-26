import pytest
import json
from website import create_app

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

def test_get_method_1(test_client):
    """Tests GET request response is valid.

    Args:
        URL Query: topic = tennis, amount = 1

    Returns:
        Test passed if Json list of size 1 with
        all relevant features is returned.

    Raises:
        Assertion error.
    """
    response = test_client.get('/request?topic=tennis&amount=1')
    summaries = json.loads(response.data)
    
    for summary in summaries:
        title = summary.get('video_title')
        channel = summary.get('channel_name')
        text = summary.get('summary')
        assert title and channel and text
    
    assert len(summaries) == 1
    return

def test_get_method_2(test_client):
    """Tests GET request response is correct for
       an invalid request.

    Args:
        URL Query: topic = football

    Returns:
        Test passed if error_code 400 is raised
        and handled, returning a json with info
        about the error.

    Raises:
        Assertion error.
    """
    response = test_client.get('/request?topic=football')
    error_codes = json.loads(response.data)

    description = error_codes.get('ERROR')
    status_code = error_codes.get('STATUS CODE')

    assert len(error_codes) == 2
    assert description and description == "GET Request failed."
    assert status_code and status_code == 400
    return


def test_get_method_3(test_client):
    """Tests GET request response is correct for
       an invalid request.

    Args:
        URL Query: amount = 1

    Returns:
        Test passed if error_code 400 is raised
        and handled, returning a json with info
        about the error.

    Raises:
        Assertion error.
    """
    response = test_client.get('/request?amount=1')
    error_codes = json.loads(response.data)

    description = error_codes.get('ERROR')
    status_code = error_codes.get('STATUS CODE')

    assert len(error_codes) == 2
    assert description and description == "GET Request failed."
    assert status_code and status_code == 400
    return

def test_get_method_4(test_client):
    """Tests GET request response is correct for
       an invalid request.

    Args:
        URL Query: None

    Returns:
        Test passed if error_code 400 is raised
        and handled, returning a json with info
        about the error.

    Raises:
        Assertion error.
    """
    response = test_client.get('/request')
    error_codes = json.loads(response.data)

    description = error_codes.get('ERROR')
    status_code = error_codes.get('STATUS CODE')

    assert len(error_codes) == 2
    assert description and description == "GET Request failed."
    assert status_code and status_code == 400
    return 

def test_get_method_5(test_client):
    """Tests GET request response is correct for
       an invalid request.

    Args:
        URL Query: topic=football, amount=0

    Returns:
        Test passed if error_code 400 is raised
        and handled, returning a json with info
        about the error.

    Raises:
        Assertion error.
    """
    response = test_client.get('/request?topic=football&amount=0')
    error_codes = json.loads(response.data)

    print(error_codes)

    description = error_codes.get('ERROR')
    status_code = error_codes.get('STATUS CODE')

    assert len(error_codes) == 2
    assert description and description == "GET Request failed."
    assert status_code and status_code == 400
    return
    
def test_get_method_6(test_client):
    """Tests GET request response is valid.

    Args:
        URL Query: topic = cars, amount = 2

    Returns:
        Test passed if Json list of size 2 with
        all relevant features is returned.

    Raises:
        Assertion error.
    """
    response = test_client.get('/request?topic=cars&amount=2')
    summaries = json.loads(response.data)

    for summary in summaries:
        title = summary.get('video_title')
        channel = summary.get('channel_name')
        text = summary.get('summary')
        assert title and channel and text
    
    assert len(summaries) == 2
    return

def test_login_required_pages_when_logged_out(test_client):
    """ Tests if pages requiring login are inaccessible when no user is logged in. Expecting
        a redirect.
    """
    response = test_client.get('/welcome')
    assert response.status_code == 302
    return