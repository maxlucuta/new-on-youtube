import pytest
import json
from flask_jwt_extended import create_access_token
from website import create_app

# headers should indicate JSON for all post requests
mimetype = 'application/json'
headers = {'Content-Type': mimetype,
           'Accept': mimetype}


@pytest.fixture(scope='module')
def test_client():
    """ Initialise fixtures to allow reuse of objects across tests
    """
    flask_app = create_app()
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client
    return


def test_request_route_with_no_amount_specified_returns_error(test_client):
    """Tests POST request response is correct for
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
    test_query = json.dumps({'topics': ['football']})
    response = test_client.post("/request", data=test_query, headers=headers)
    response = json.loads(response.data)

    status_code = response['status_code']
    description = response['description']

    assert status_code and status_code == 400
    assert description and description == "Missing payload fields"
    return


def test_request_route_with_no_topic_specified_returns_error(test_client):
    """Tests POST request response is correct for
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
    test_query = json.dumps({'amount': '1'})
    response = test_client.post("/request", data=test_query, headers=headers)
    response = json.loads(response.data)

    status_code = response['status_code']
    description = response['description']

    assert status_code and status_code == 400
    assert description and description == "Missing payload fields"
    return


def test_request_route_with_zero_amount_returns_error(test_client):
    """Tests POST request response is correct for
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
    test_query = json.dumps({'topic': ['football'], 'amount': '0'})
    response = test_client.post("/request", data=test_query, headers=headers)
    response = json.loads(response.data)

    status_code = response['status_code']
    description = response['description']

    assert status_code and status_code == 400
    assert description and description == "Missing payload fields"
    return


def test_valid_request_can_return_one_video_with_required_fields(test_client):
    """Tests POST request response is valid.
    Args:
        URL Query: topic = tennis, amount = 1
    Returns:
        Test passed if Json list of size 1 with
        all relevant features is returned.
    Raises:
        Assertion error.
    """
    test_query = json.dumps({'topics': ['tennis'], 'amount': 1})
    response = test_client.post("/request", data=test_query, headers=headers)
    response = json.loads(response.data)

    assert response['status_code'] == 200
    summaries = response['results']

    for summary in summaries:
        title = summary['video_title']
        channel = summary['channel_name']
        summary_text = summary['summary']
        views = summary['views']
        likes = summary['likes']
        published_at = summary['published_at']
        video_id = summary['video_id']
        keyword = summary['keyword']

        assert title
        assert channel
        assert summary_text
        assert views
        assert likes
        assert published_at
        assert video_id
        assert keyword

    assert len(summaries) == 1
    return


def test_valid_request_returns_requested_number_of_videos(test_client):
    """Tests POST request response is valid.
    Args:
        URL Query: topic = cars, amount = 2
    Returns:
        Test passed if Json list of size 2 with
        all relevant features is returned.
    Raises:
        Assertion error.
    """
    test_query = json.dumps({'topics': ['joe rogan'], 'amount': '4'})
    response = test_client.post("/request", data=test_query, headers=headers)
    response = json.loads(response.data)

    assert response['status_code'] == 200
    summaries = response['results']

    for summary in summaries:
        title = summary['video_title']
        channel = summary['channel_name']
        summary_text = summary['summary']
        views = summary['views']
        likes = summary['likes']
        published_at = summary['published_at']
        video_id = summary['video_id']
        keyword = summary['keyword']

        assert title
        assert channel
        assert summary_text
        assert views
        assert likes
        assert published_at
        assert video_id
        assert keyword

    assert len(summaries) == 4
    return


def test_request_route_topic_is_not_case_sensitive(test_client):
    """Tests POST request response is valid.
    Args:
        URL Query: topic = cars, amount = 2
    Returns:
        Test passed if Json list of size 2 with
        all relevant features is returned.
    Raises:
        Assertion error.
    """
    test_query = json.dumps({'topics': ['JoE RoGAn'], 'amount': '1'})
    response = test_client.post("/request", data=test_query, headers=headers)
    response = json.loads(response.data)
    print(type(response))
    assert response['status_code'] == 200
    summaries = response['results']

    assert len(summaries) == 1
    return


def test_request_user_topics_with_valid_username(test_client):
    access_token = create_access_token('testuser')
    headers_logged_in = {'Content-Type': mimetype,
                         'Accept': mimetype,
                         'Authorization': 'Bearer {}'.format(access_token)}

    test_query = json.dumps({'username': "devuser4"})

    response = test_client.post(
        "/get_user_topics", data=test_query, headers=headers_logged_in)
    response = json.loads(response.data)

    status_code = response['status_code']
    assert status_code == 200

    results = response['results']
    assert len(results) > 0
    return


def test_request_user_topics_with_invalid_username(test_client):
    access_token = create_access_token('testuser')
    headers_logged_in = {'Content-Type': mimetype,
                         'Accept': mimetype,
                         'Authorization': 'Bearer {}'.format(access_token)}

    test_query = json.dumps({'username': "invalidusername_fdahkfndoivena"})

    response = test_client.post(
        "/get_user_topics", data=test_query, headers=headers_logged_in)
    response = json.loads(response.data)

    status_code = response['status_code']
    description = response['description']

    assert status_code and status_code == 500
    assert description and description == 'username not found in database'
    return


def test_user_request_with_missing_amount_returns_error(test_client):
    access_token = create_access_token('testuser')
    headers_logged_in = {'Content-Type': mimetype,
                         'Accept': mimetype,
                         'Authorization': 'Bearer {}'.format(access_token)}

    test_query = json.dumps({'username': "invalidusername_fdhjlafjndladfs",
                             'sort_by': "Random"})

    response = test_client.post(
        "/user_request", data=test_query, headers=headers_logged_in)
    response = json.loads(response.data)

    status_code = response['status_code']
    description = response['description']

    assert status_code and status_code == 400
    assert description and description == 'Missing payload fields'
    return


def test_user_request_with_invalid_username_returns_error(test_client):
    access_token = create_access_token('testuser')
    headers_logged_in = {'Content-Type': mimetype,
                         'Accept': mimetype,
                         'Authorization': 'Bearer {}'.format(access_token)}

    test_query = json.dumps({'username': "invalidusername_fdhjlafjndladfs",
                             'amount': 10,
                             'sort_by': "Random"})

    response = test_client.post(
        "/user_request", data=test_query, headers=headers_logged_in)
    response = json.loads(response.data)

    status_code = response['status_code']
    description = response['description']

    assert status_code and status_code == 500
    assert description and description == 'username not found in database'
    return


def test_user_request_with_no_amount_returns_error(test_client):
    access_token = create_access_token('testuser')
    headers_logged_in = {'Content-Type': mimetype,
                         'Accept': mimetype,
                         'Authorization': 'Bearer {}'.format(access_token)}

    test_query = json.dumps({'username': "devuser4",
                             'amount': 0,
                             'sort_by': "Random"})

    response = test_client.post(
        "/user_request", data=test_query, headers=headers_logged_in)
    response = json.loads(response.data)

    status_code = response['status_code']
    description = response['description']

    assert status_code and status_code == 400
    assert description and description == "Invalid payload fields"
    return


def test_valid_user_request_returns_requested_number_of_videos(test_client):
    access_token = create_access_token('testuser')
    headers_logged_in = {'Content-Type': mimetype,
                         'Accept': mimetype,
                         'Authorization': 'Bearer {}'.format(access_token)}

    test_query = json.dumps({'username': "devuser4",
                             'amount': 5,
                             'sort_by': "Random"})

    response = test_client.post(
        "/user_request", data=test_query, headers=headers_logged_in)
    response = json.loads(response.data)

    assert response['status_code'] == 200
    summaries = response['results']

    for summary in summaries:
        title = summary['video_title']
        channel = summary['channel_name']
        summary_text = summary['summary']
        views = summary['views']
        likes = summary['likes']
        published_at = summary['published_at']
        video_id = summary['video_id']
        keyword = summary['keyword']

        assert title
        assert channel
        assert summary_text
        assert views
        assert likes
        assert published_at
        assert video_id
        assert keyword

    assert len(summaries) == 5
    return


def test_valid_user_request_returns_requested_recommended_videos(test_client):
    access_token = create_access_token('testuser')
    headers_logged_in = {'Content-Type': mimetype,
                         'Accept': mimetype,
                         'Authorization': 'Bearer {}'.format(access_token)}

    test_query = json.dumps({'username': "devuser4",
                             'amount': 5,
                             'sort_by': "Recommended"})

    response = test_client.post(
        "/user_request", data=test_query, headers=headers_logged_in)
    response = json.loads(response.data)

    assert response['status_code'] == 200
    summaries = response['results']

    for summary in summaries:
        title = summary['video_title']
        channel = summary['channel_name']
        summary_text = summary['summary']
        views = summary['views']
        likes = summary['likes']
        published_at = summary['published_at']
        video_id = summary['video_id']
        keyword = summary['keyword']

        assert title
        assert channel
        assert summary_text
        assert views
        assert likes
        assert published_at
        assert video_id
        assert keyword

    assert len(summaries) > 0
    return


def test_get_user_topics_without_username_returns_error(test_client):
    access_token = create_access_token('testuser')
    headers_logged_in = {'Content-Type': mimetype,
                         'Accept': mimetype,
                         'Authorization': 'Bearer {}'.format(access_token)}

    test_query = json.dumps({'amount': 5,
                             'sort_by': "Recommended"})

    response = test_client.post(
        "/get_user_topics", data=test_query, headers=headers_logged_in)
    response = json.loads(response.data)

    status_code = response['status_code']
    description = response['description']

    assert status_code and status_code == 400
    assert description and description == 'Missing payload fields'
    return


def test_get_user_topics_with_invalid_username_returns_error(test_client):
    access_token = create_access_token('testuser')
    headers_logged_in = {'Content-Type': mimetype,
                         'Accept': mimetype,
                         'Authorization': 'Bearer {}'.format(access_token)}

    test_query = json.dumps({'username': "invaliduser_dfhpaknodvnafvdasfdase",
                             'amount': 5,
                             'sort_by': "Recommended"})

    response = test_client.post(
        "/get_user_topics", data=test_query, headers=headers_logged_in)
    response = json.loads(response.data)

    status_code = response['status_code']

    assert status_code and status_code == 500
    return


def test_get_user_topics_returns_valid_response(test_client):
    access_token = create_access_token('testuser')
    headers_logged_in = {'Content-Type': mimetype,
                         'Accept': mimetype,
                         'Authorization': 'Bearer {}'.format(access_token)}

    test_query = json.dumps({'username': "devuser4",
                             'amount': 5,
                             'sort_by': "Recommended"})

    response = test_client.post(
        "/get_user_topics", data=test_query, headers=headers_logged_in)
    response = json.loads(response.data)

    assert response['status_code'] == 200
    topics = response['results']

    assert len(topics) > 0
    return


def test_update_user_topics_without_username_returns_error(test_client):
    access_token = create_access_token('testuser')
    headers_logged_in = {'Content-Type': mimetype,
                         'Accept': mimetype,
                         'Authorization': 'Bearer {}'.format(access_token)}

    test_query = json.dumps({'topics': "placeholder_topic"})

    response = test_client.post(
        "/update_user_topics", data=test_query, headers=headers_logged_in)
    response = json.loads(response.data)

    status_code = response['status_code']
    description = response['description']

    assert status_code and status_code == 400
    assert description and description == 'Missing payload fields'
    return


def test_update_user_topics_updates_user_topics(test_client):
    access_token = create_access_token('testuser')
    headers_logged_in = {'Content-Type': mimetype,
                         'Accept': mimetype,
                         'Authorization': 'Bearer {}'.format(access_token)}

    test_query = json.dumps({'username': "devuser4",
                             'topics': "f1"})

    response = test_client.post(
        "/update_user_topics", data=test_query, headers=headers_logged_in)
    response = json.loads(response.data)

    status_code = response['status_code']

    assert status_code and status_code == 200
    return


def test_update_user_watched_vids_without_username_returns_error(test_client):
    access_token = create_access_token('testuser')
    headers_logged_in = {'Content-Type': mimetype,
                         'Accept': mimetype,
                         'Authorization': 'Bearer {}'.format(access_token)}

    test_query = json.dumps({'topic': "f1",
                             'video_id': "aouCUd_NcmE"})

    response = test_client.post(
        "/update_user_watched_videos",
        data=test_query,
        headers=headers_logged_in)
    response = json.loads(response.data)

    status_code = response['status_code']
    description = response['description']

    assert status_code and status_code == 400
    assert description and description == 'Missing payload fields'
    return


def test_update_user_watched_vids_without_vid_ID_returns_error(test_client):
    access_token = create_access_token('testuser')
    headers_logged_in = {'Content-Type': mimetype,
                         'Accept': mimetype,
                         'Authorization': 'Bearer {}'.format(access_token)}

    test_query = json.dumps({'username': "devuser4",
                             'topic': "f1"})

    response = test_client.post(
        "/update_user_watched_videos",
        data=test_query,
        headers=headers_logged_in)
    response = json.loads(response.data)

    status_code = response['status_code']
    description = response['description']

    assert status_code and status_code == 400
    assert description and description == 'Missing payload fields'
    return


def test_update_user_watched_vids_without_topic_returns_error(test_client):
    access_token = create_access_token('testuser')
    headers_logged_in = {'Content-Type': mimetype,
                         'Accept': mimetype,
                         'Authorization': 'Bearer {}'.format(access_token)}

    test_query = json.dumps({'username': "devuser4",
                             'video_id': "aouCUd_NcmE"})

    response = test_client.post(
        "/update_user_watched_videos",
        data=test_query,
        headers=headers_logged_in)
    response = json.loads(response.data)

    status_code = response['status_code']
    description = response['description']

    assert status_code and status_code == 400
    assert description and description == 'Missing payload fields'
    return
