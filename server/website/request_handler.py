"""Important information:

Implementation routes front-end POST requests to /request,
it is the front-end developers responsibility to ensure
that the request contains both topic=x and amount=y,
otherwise an error code will be returned.
"""
from flask import Blueprint, request, abort
from .utilities.database import query_yt_videos
from .utilities.database import query_users_db
from .utilities.database import update_user_topics_in_db
from .utilities.database import user_feed_query
from .utilities.database import add_videos_by_topic_to_db
from flask_jwt_extended import jwt_required
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
            query_response['video_title']
            query_response['views']
            query_response['summary']
            query_response['video_id']
            query_response['likes']
            query_response['published_at']
        except KeyError:
            return False

    return True


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


@request_blueprint.route("/user_request", methods=['POST'])
@jwt_required()
def user_request_summary():
    """ Retrieves sorted summarised transcripts for a list of topics.
    Args:
            json: POST request -> username, topics, and sorted method extracted
                   from json
    Returns:
            response: List of dicts, one for each returned video. Each of
                      which contains 'keyword', 'likes', 'video_title',
                      'published_at', 'video_id', 'summary', 'channel_name'
    Raises:
            HTTPException 400 / 404 / 408 / 417 / 500
    """

    body = request.get_json()
    try:
        username = body["username"]
        amount = body["amount"]
        sort_by = body["sort_by"]
    except KeyError:
        abort(400)

    user = query_users_db(username)
    if not user:
        return {'status_code': 500, 'description': 'database request failed'}
    topics = user.topics

    validate_get_request(topics, amount)

    response = user_feed_query(topics, amount, sort_by)

    if not valid_query_response(response, int(amount)):
        abort(417)

    return {'status_code': 200, 'description': 'Ok.', 'results': response}

# To be removed - don't think we need this anymore


@request_blueprint.route("/popular_videos", methods=['GET'])
def popular_videos():
    results = query_yt_videos("football", 10)

    if not valid_query_response(results, len(results)):
        abort(417)

    return {'status_code': 200, 'description': 'Ok.', 'results': results}


@request_blueprint.route("/get_user_topics", methods=['POST'])
@jwt_required()
def get_user_topics():
    try:
        username = request.json["username"]
    except KeyError:
        abort(400)
    user = query_users_db(username)
    if not user:
        return {'status_code': 500, 'description': 'database request failed'}
    results = user.topics
    return {'status_code': 200, 'description': 'Ok.', 'results': results}


@request_blueprint.route("/update_user_topics", methods=['POST'])
@jwt_required()
def update_user_topics():
    try:
        username = request.json["username"]
        topics = request.json["topics"]
    except KeyError:
        abort(400)
    if not update_user_topics_in_db(username, topics):
        return {'status_code': 500, 'description': 'database update failed'}
    add_videos_by_topic_to_db(topics)
    return {'status_code': 200, 'description': 'Ok.'}
