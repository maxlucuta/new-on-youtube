"""Important information:

Implementation routes front-end POST requests to /request,
it is the front-end developers responsibility to ensure
that the request contains both topic=x and amount=y,
otherwise an error code will be returned.
"""
from flask import Blueprint, request, abort
from .utilities.database import query_yt_videos
from flask_login import current_user
import random

request_blueprint = Blueprint("request_blueprint", __name__)


@request_blueprint.errorhandler(400)
def bad_request(e):
    """ Handles HTTPException code 400.
            Returns: dict containing error description
                             and status code.
    """
    return {
        'status_code': 400,
        'description': 'POST Request failed.',
        'results': []
    }


@request_blueprint.errorhandler(404)
def not_found(e):
    """ Handles HTTPException code 404.
            Returns: dict containing error description
                             and status code.
    """
    return {
        'status_code': 404,
        'description': 'Topic not found.',
        'results': []
    }


@request_blueprint.errorhandler(408)
def timeout(e):
    """ Handles HTTPException code 408.
            Returns: dict containing error description
                             and status code.
    """
    return {
        'status_code': 408,
        'description': 'Database connection timed out.',
        'results': []
    }


@request_blueprint.errorhandler(417)
def query_failure(e):
    """ Handles HTTPException code 417.
            Returns: dict containing error description
                             and status code.
    """
    return {
        'status_code': 417,
        'description': 'Unable to fetch request from database.',
        'results': []
    }


@request_blueprint.errorhandler(500)
def server_error(e):
    """ Handles HTTPException code 500.
            Returns: dict containing error description
                             and status code.
    """
    return {
        'status_code': 500,
        'description': 'Database connection failiure.',
        'results': []
    }


def validate_get_request(topics, amount):
    """Checks if the POST request params are valid.
    Args:
            topic: string denoting topic to query.
            amount: int denoting number of expected responses.

    Returns:
            True if request is valid.
            False if request is invalid.
    """
    if not topics or not amount:
        abort(400)

    valid_topics = True
    # for topic in topics:
    #     valid_topics &= bool(re.match(r'[a-zA-Z\s]+$', topic))

    if not valid_topics or not str(amount).isdigit() \
            or 0 >= int(amount) or int(amount) > 20:
        abort(400)


def valid_query_response(topic_summaries, amount):
    """Checks if the POST response satisfies the request.
    Args:
            topic_summaries: [{dict}] containing query response.
            amount: int denoting number of expected responses.

    Returns:
            True if response is valid.
            False if response is incomplete.
    """
    for query_response in topic_summaries:
        try:
            query_response.get('video_title')
            query_response.get('channel_name')
            query_response.get('summary')
            query_response.get('video_id')
        except KeyError:
            return False

    return True
    # return len(topic_summaries) == amount


@request_blueprint.route("/", methods=['POST'])
@request_blueprint.route("/home", methods=['POST'])
@request_blueprint.route("/request", methods=['POST'])
def request_summary():
    """ Retrieves summarised transcripts for a topic.
    Args:
            topic: GET request -> topic extracted through URL
                       query parameters as string.
            amount: Included in GET URL query parameters,
                       denotes number of summaries to be retrieved.
    Returns:
            summary: { video : vid_title, channel : channel_name, summary : s }
                            dict with key : val bring string : string.
                            Dict is of k * 3 elements where k is number of
                            videos in amount.
    Raises:
            HTTPException 400 / 404 / 408 / 417 / 500
    """

    body = request.get_json()
    try:
        topics = body["topics"]
        amount = body["amount"]
    except KeyError:
        abort(400)

    # topics = request.form.getlist('topics', type=str)
    # amount = request.form.get('amount')

    validate_get_request(topics, amount)

    response = []
    for topic in topics:
        query_response = (query_yt_videos(topic, int(amount)))
        response += query_response

    random.shuffle(response)
    response = response[:int(amount)]
    if not valid_query_response(response, int(amount)):
        abort(417)

    return {'status_code': 200, 'description': 'Ok.', 'results': response}


@request_blueprint.route("/popular_videos", methods=['GET'])
def popular_videos():
    results = query_yt_videos("football", 10)

    if not valid_query_response(results, len(results)):
        abort(417)

    return {'status_code': 200, 'description': 'Ok.', 'results': results}


@request_blueprint.route("/user_topics", methods=['POST'])
def get_user_topics():
    if not current_user.is_authenticated:
        return {'status_code': 417, 'description': 'Currently no user logged in', 'results': []}
    results = current_user.topics
    return {'status_code': 200, 'description': 'Ok.', 'results': results}
